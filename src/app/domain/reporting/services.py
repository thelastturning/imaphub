class GAQLService:
    """
    Builder for Google Ads Query Language (GAQL).
    Specific logic to handle segmentation rules and status mappings.
    """
    
    @staticmethod
    def build_search_term_query(lookback_days: int = 30) -> str:
        """
        Constructs the high-volume search term view query.
        """
        return f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            segments.keyword.info.text,
            metrics.clicks,
            metrics.impressions,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{lookback_days}_DAYS
          AND metrics.impressions > 0
        """

    @staticmethod
    def build_campaign_sync_query() -> str:
        """
        Query for syncing Campaign structure (No segments).
        """
        return """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign.start_date,
            campaign.end_date,
            campaign.serving_status
        FROM campaign
        WHERE campaign.status != "REMOVED"
        """
