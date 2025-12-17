from typing import List, Any, Optional
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient

class GoogleAdsMutator:
    """
    Handles Google Ads Mutations with intelligent Policy Error handling.
    Implements the 'Try-Catch-Exempt' pattern for resilient syncing.
    """
    def __init__(self, google_ads_client: GoogleAdsClient, customer_id: str):
        self.client = google_ads_client
        self.customer_id = customer_id
        
        # Services
        self.campaign_service = self.client.get_service("CampaignService")
        self.ad_group_service = self.client.get_service("AdGroupService")
        self.ad_service = self.client.get_service("AdGroupAdService")

    def _create_exemption_policy(self, policy_finding_details) -> List[Any]:
        """
        Extracts policy keys from error details to create exemptions.
        """
        exemptions = []
        for entry in policy_finding_details.policy_topic_entries:
            # We only exempt if it's explicitly 'exemptible' or we decide to force it
            # For this implementation, we try to exempt everything returned as a finding
            if entry.type_ != self.client.enums.PolicyTopicEntryTypeEnum.PROHIBITED:
                 key = self.client.get_type("PolicyViolationKey")
                 key.policy_topic = entry.topic
                 key.violating_text = entry.violating_text
                 exemptions.append(key)
        return exemptions

    def sync_campaign(self, campaign_operation, attempt=1, max_attempts=3):
        """
        Syncs a Campaign with retry logic.
        """
        request = self.client.get_type("MutateCampaignsRequest")
        request.customer_id = self.customer_id
        request.operations.append(campaign_operation)

        try:
            return self.campaign_service.mutate_campaigns(request=request)
        except GoogleAdsException as ex:
            # Campaign level violations are rare (usually name duplication etc)
            raise ex

    def sync_ad_group(self, ad_group_operation):
        request = self.client.get_type("MutateAdGroupsRequest")
        request.customer_id = self.customer_id
        request.operations.append(ad_group_operation)
        return self.ad_group_service.mutate_ad_groups(request=request)

    def sync_rsa_ad(self, ad_operation, attempt=1, max_attempts=3):
        """
        Syncs an RSA Ad with specific "Try-Catch-Exempt" logic for text policies.
        """
        request = self.client.get_type("MutateAdGroupAdsRequest")
        request.customer_id = self.customer_id
        request.operations.append(ad_operation)

        try:
            # Attempt 1: Standard Push
            return self.ad_service.mutate_ad_group_ads(request=request)
        except GoogleAdsException as ex:
            if attempt >= max_attempts:
                raise ex

            # Analyze for Policy Findings
            ignorable_policy_topics = []
            has_exemptible_error = False

            for error in ex.failure.errors:
                if error.error_code.policy_finding_error == self.client.enums.PolicyFindingErrorEnum.POLICY_FINDING:
                     if getattr(error.details, "policy_finding_details", None):
                        keys = self._create_exemption_policy(error.details.policy_finding_details)
                        ignorable_policy_topics.extend(keys)
                        has_exemptible_error = True

            if has_exemptible_error and ignorable_policy_topics:
                print(f"Policy Violation Detected. Applying {len(ignorable_policy_topics)} exemptions and Retrying...")
                
                # Apply exemptions to the operation's policy validation parameter
                # Note: This sits on the OPERATION.policy_validation_parameter
                
                # Ensure the parameter object exists
                if not ad_operation.policy_validation_parameter:
                    ad_operation.policy_validation_parameter = self.client.get_type("PolicyValidationParameter")
                
                ad_operation.policy_validation_parameter.ignorable_policy_topics.extend(ignorable_policy_topics)
                
                # Recursive Retry
                return self.sync_rsa_ad(ad_operation, attempt=attempt+1, max_attempts=max_attempts)
            
            # If not a policy finding error, re-raise
            raise ex
