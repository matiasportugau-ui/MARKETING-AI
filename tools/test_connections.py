import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_google_ads():
    print("\n[TEST] Google Ads Integration...")
    dev_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")

    if not dev_token or not client_id:
        print("❌ SKIPPED: Missing GOOGLE_ADS_DEVELOPER_TOKEN or CLIENT_ID in .env")
        return

    try:
        from google.ads.googleads.client import GoogleAdsClient
        from google.ads.googleads.errors import GoogleAdsException

        # Initialize client using env vars (standard Google Ads SDK behavior)
        # Note: The SDK typically looks for a dictionary configuration or specific env vars.
        # We manually construct the config dict here to be explicit.
        config = {
            "developer_token": dev_token,
            "client_id": client_id,
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True,
        }

        client = GoogleAdsClient.load_from_dict(config, version="v17")
        ga_service = client.get_service("GoogleAdsService")
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID").replace("-", "")

        # Simple query: Get Campaign Names
        query = """
            SELECT campaign.id, campaign.name 
            FROM campaign 
            WHERE campaign.status != 'REMOVED' 
            LIMIT 3
        """

        stream = ga_service.search_stream(customer_id=customer_id, query=query)

        print("✅ SUCCESS: Connected to Google Ads.")
        count = 0
        for batch in stream:
            for row in batch.results:
                print(
                    f"   - Found Campaign: {row.campaign.name} (ID: {row.campaign.id})"
                )
                count += 1
        if count == 0:
            print("   (No active campaigns found, but connection works)")

    except ImportError:
        print(
            "❌ ERROR: google-ads library not installed. Run 'pip install google-ads'"
        )
    except Exception as e:
        print(f"❌ ERROR: Connection failed. {str(e)}")


def test_meta_ads():
    print("\n[TEST] Meta (Facebook) Integration...")
    access_token = os.getenv("META_ACCESS_TOKEN")
    app_id = os.getenv("META_APP_ID")
    ad_account_id = os.getenv("META_AD_ACCOUNT_ID")

    if not access_token or not ad_account_id:
        print("❌ SKIPPED: Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID in .env")
        return

    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.adobjects.campaign import Campaign

        FacebookAdsApi.init(
            access_token=access_token, app_id=app_id, api_version="v19.0"
        )

        account = AdAccount(ad_account_id)
        campaigns = account.get_campaigns(
            fields=[Campaign.Field.name, Campaign.Field.status], params={"limit": 3}
        )

        print("✅ SUCCESS: Connected to Meta Ads.")
        for campaign in campaigns:
            print(f"   - Found Campaign: {campaign['name']} ({campaign['status']})")

    except ImportError:
        print(
            "❌ ERROR: facebook-business library not installed. Run 'pip install facebook-business'"
        )
    except Exception as e:
        print(f"❌ ERROR: Connection failed. {str(e)}")


if __name__ == "__main__":
    print("Gravity API Connection Tester")
    print("=============================")
    test_google_ads()
    test_meta_ads()
    print("\nDone.")
