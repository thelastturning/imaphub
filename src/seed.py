import time
import sys
from arango import ArangoClient
from arango.exceptions import ServerConnectionError

def wait_for_db(url, retries=30, delay=2):
    client = ArangoClient(hosts=url)
    for i in range(retries):
        try:
            sys_db = client.db('_system', username='root', password='')
            sys_db.version()
            print(f"Connected to ArangoDB at {url}")
            return client
        except ServerConnectionError as e:
            print(f"Waiting for ArangoDB... ({i+1}/{retries}) - {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error connecting: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to ArangoDB")

def seed():
    # Connect
    # Note: Host is 'db' as per docker-compose service name, port 8529
    client = wait_for_db('http://db:8529')

    # Create Database
    db_name = 'imap_campaign_wizard'
    sys_db = client.db('_system', username='root', password='')
    
    if not sys_db.has_database(db_name):
        sys_db.create_database(db_name)
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    db = client.db(db_name, username='root', password='')

    # Collections
    doc_collections = ['Campaigns', 'AdGroups', 'Assets']
    edge_collections = ['belongs_to', 'uses_asset']

    for col in doc_collections:
        if not db.has_collection(col):
            db.create_collection(col)
            print(f"Collection '{col}' created.")

    for col in edge_collections:
        if not db.has_collection(col):
            db.create_collection(col, edge=True)
            print(f"Edge Collection '{col}' created.")

    # Data - Campaigns
    campaigns_data = [
        {"_key": "c1", "name": "Webinar HR Transformation", "status": "ACTIVE"},
        {"_key": "c2", "name": "Whitepaper KI im Marketing", "status": "PAUSED"}
    ]
    
    campaigns = db.collection('Campaigns')
    for c in campaigns_data:
        if not campaigns.has(c['_key']):
            campaigns.insert(c)
            print(f"Campaign '{c['name']}' inserted.")

    # Data - AdGroups
    # 2 AdGroups per Campaign
    adgroups_data = [
        {"_key": "ag1", "name": "Target HR Managers", "campaign_key": "c1"},
        {"_key": "ag2", "name": "Target CTOs", "campaign_key": "c1"},
        {"_key": "ag3", "name": "Target CMOs", "campaign_key": "c2"},
        {"_key": "ag4", "name": "Target Marketing Leads", "campaign_key": "c2"}
    ]

    adgroups = db.collection('AdGroups')
    belongs_to = db.collection('belongs_to')

    for ag in adgroups_data:
        if not adgroups.has(ag['_key']):
            camp_key = ag.pop('campaign_key')
            # Insert AdGroup
            adgroups.insert(ag)
            print(f"AdGroup '{ag['name']}' inserted.")
            
            # Create Edge: AdGroup -> Campaign (belongs_to)
            # Assuming direction: AdGroup belongs to Campaign
            # Or Campaign has AdGroups? Usually AdGroup -> belongs_to -> Campaign
            # Let's verify standard pattern. "belongs_to" usually implies Child -> Parent.
            # So _from: AdGroups/key, _to: Campaigns/key
            edge = {
                "_from": f"AdGroups/{ag['_key']}",
                "_to": f"Campaigns/{camp_key}",
                "type": "belongs_to"
            }
            belongs_to.insert(edge)
            print(f"Edge AdGroup/{ag['_key']} -> Campaigns/{camp_key} created.")

    # Data - Assets
    assets_data = [
        {"_key": "as1", "type": "Headline", "text": "Transform HR Now"},
        {"_key": "as2", "type": "Description", "text": "Join our potential webinar."},
        {"_key": "as3", "type": "Headline", "text": "Unlock AI Potential"},
        {"_key": "as4", "type": "Description", "text": "Download the whitepaper today."}
    ]

    assets = db.collection('Assets')
    uses_asset = db.collection('uses_asset')

    for a in assets_data:
        if not assets.has(a['_key']):
            assets.insert(a)
            print(f"Asset '{a['text']}' inserted.")

    # Link Assets to AdGroups (uses_asset)
    # AdGroup uses Asset
    # _from: AdGroups/key, _to: Assets/key
    links = [
        ("ag1", "as1"), ("ag1", "as2"),
        ("ag2", "as1"),
        ("ag3", "as3"), ("ag3", "as4"),
        ("ag4", "as3")
    ]

    for ag_key, as_key in links:
        # Check uniqueness if needed, or just insert blind for seed (allows duplicates if run multiple times without cleanup? arango keys are unique but edges are not unless keys provided)
        # We'll query to check existence to be safe or just use a deterministic key
        edge_key = f"{ag_key}_{as_key}"
        if not uses_asset.has(edge_key):
             edge = {
                "_key": edge_key,
                "_from": f"AdGroups/{ag_key}",
                "_to": f"Assets/{as_key}"
            }
             uses_asset.insert(edge)
             print(f"Edge AdGroups/{ag_key} -> Assets/{as_key} created.")

if __name__ == "__main__":
    print("Starting seed process...")
    try:
        seed()
        print("Seed completed successfully.")
    except Exception as e:
        print(f"Seed failed: {e}")
        sys.exit(1)
