import requests

url = "https://stockx.com/api/p/e"

payload = {
    "query": "query FetchProductCollection($id: String, $country: String!, $currencyCode: CurrencyCode!, $limit: Int!, $marketName: String, $skipFollowed: Boolean!) { productCollection(id: $id) {   tileType   priceType   footnotesType   trackingEvent   helpMessage   products(page: 0, limit: $limit) {     ... on ProductsConnection {       edges {         node {           id           title           productCategory           name           urlKey           uuid           ...FollowedFragment @skip(if: $skipFollowed)           variants {             id           }           media {             smallImageUrl           }           ...XpressAskFragment           market(currencyCode: $currencyCode) {             bidAskData(country: $country, market: $marketName) {               highestBid               lastHighestBidTime               lastLowestAskTime               lowestAsk             }             salesInformation {               lastSale               salesThisPeriod             }             deadStock {               sold             }           }           traits(filterTypes: [RELEASE_DATE]) {             name             value           }         }       }     }   }   seeAllCTA {     title     url     urlType   }   title }\n}\n\nfragment XpressAskFragment on Product { market(currencyCode: $currencyCode) {   state(country: $country) {     numberOfCustodialAsks   } }\n}\n\nfragment FollowedFragment on Product { followed}",
    "variables": {
        "id": "blt3918c5dcebdbd12c",
        "limit": 6,
        "country": "US",
        "currencyCode": "USD",
        "marketName": "US",
        "skipFollowed": True
    },
    "operationName": "FetchProductCollection"
}
headers = {
    "cookie": "stockx_device_id=28e9059b-3395-46a2-9813-e97ddd7662d1; _pxvid=a9de775a-4463-11ed-afc6-7361536b7945; _ga=undefined; __pxvid=a9feb6e5-4463-11ed-8c5a-0242ac120002; _gcl_au=1.1.1033908152.1664943039; _ga=GA1.2.431278022.1664943039; _gac_UA-67038415-1=1.1664943039.CjwKCAjws--ZBhAXEiwAv-RNLzUsm6HAuFRDf_s1zT7Vearcxql4w2Gq3htn-TuRaTSsbvHPXPvbdxoCjWAQAvD_BwE; ajs_anonymous_id=6dec30a6-7f85-449b-8cbe-2574875901a4; _gcl_aw=GCL.1664943040.CjwKCAjws--ZBhAXEiwAv-RNLzUsm6HAuFRDf_s1zT7Vearcxql4w2Gq3htn-TuRaTSsbvHPXPvbdxoCjWAQAvD_BwE; _gcl_dc=GCL.1664943040.CjwKCAjws--ZBhAXEiwAv-RNLzUsm6HAuFRDf_s1zT7Vearcxql4w2Gq3htn-TuRaTSsbvHPXPvbdxoCjWAQAvD_BwE; _pin_unauth=dWlkPVpUZGtNelJtT1RrdE5qVXpZUzAwTURKakxXSXpOREl0T1dZMFlXWmlPREUzWm1ZMg; _clck=1jwnzzj|1|f5g|0; rbuid=rbos-17fdf9d5-c052-4dc5-b2b8-8eaca491903f; __ssid=ccdb1ffbad79936184229a77179a4e3; rskxRunCookie=0; rCookie=7dsni18johryxlbd3efnkl8v43k0y; QuantumMetricUserID=4bab962beb34aad429478a2e928b51bc; OptanonAlertBoxClosed=2022-10-05T04:10:42.648Z; __pdst=92e2554b463d4c4fbb204c67c9b7e6fd; _rdt_uuid=1664943043250.665558b8-f4b9-4726-bb60-adfe2a48a54d; stockx_homepage=sneakers; tracker_device=1baba2bb-fb7c-437a-99e7-92d06c2e07f6; language_code=en; stockx_selected_region=US; pxcts=01e9ff22-54d1-11ed-958d-6f6f57434c66; stockx_preferred_market_activity=sales; IR_gbd=stockx.com; stockx_product_visits=4; stockx_session=1a1635fd-9d1f-450f-ba47-9c76e24a8d72; __cf_bm=Ad7L9kDxg.X5ouwwygknQ6wJCJFzYHwa8KidDpq2kF0-1667286066-0-AV/XWTBTINfTcfRVgJ49W5SqfMi9nNnDCJ/q3AI3SmSQYKBRmAewBxvnyGXNBz56OAv+jjzB/IE7BiJzFv+8qyc=; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Nov+01+2022+00%3A01%3A08+GMT-0700+(Pacific+Daylight+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=b2bfa940-2f08-4767-a42e-4a473512b1a2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&geolocation=US%3BCA&AwaitingReconsent=false; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_idp_c=1,s; _pxff_fed=5000; _gid=GA1.2.1808381509.1667286069; _gat=1; _px3=d7bc18d0089cc857b2bbb29a971bb35086f5551364866d4b4333fb8fe0fcf3d9:fcmGAOsjyAdaj6JjaBdh/DGCQc210rCdeMLCcOLHGUkc31j29MIyRSBQV7erWkszQ+0sRQ1AHj0Gc7sMNKWiNw==:1000:BS8nb5bCKtED8qQc1suzEroDL/QiwlEtPE08b48vssOiIR+2o4s4V/P7NBznNqhhWemjC8VwWXw5sXNABhu0V91T5DWOZy84L0UWnbRxx/QsdPnKJ2maXTZPnkbFKFGP1XT+IBgkdFNZjtkaGPokn/cx6Um102xQRGmScG81jhw+9ahoDlcNk5dlp0e30llNRs3KxEVQDMvhidrWP83GlZtJL22eNScgA7TajND48e0=; forterToken=3f6702817d4644a6b8cc7e121428f24d_1667286068970__UDF43_13ck; _derived_epik=dj0yJnU9aDB6LVpHM19oTXJXUDUwcWY1NWVOZUJEdUJjOXhWNGsmbj05M19IVW1hVFBWbGczRm1JQ3k0WDBnJm09MSZ0PUFBQUFBR05neERrJnJtPTEmcnQ9QUFBQUFHTmd4RGsmc3A9Mg; _uetsid=f862bbb059b211eda272e3de7cb6ef6c; _uetvid=ac191ea0446311eda4e589601b02f195; IR_9060=1667286073653%7C0%7C1667286073653%7C%7C; IR_PI=ae42d548-4463-11ed-95b1-b3c601db7107%7C1667372473653; lastRskxRun=1667286077162; QuantumMetricSessionID=9439f78c3fb0a99d6547f475a98bbae8; _pxde=41aaf4b82f9c43e2088059d76410c039f2e8f09a3cd8ab717f9279bd559ab922:eyJ0aW1lc3RhbXAiOjE2NjcyODYwODQwODUsImZfa2IiOjB9; _dd_s=rum=0&expire=1667286984633",
    "authority": "stockx.com",
    "accept": "*/*",
    "accept-language": "en-US",
    "apollographql-client-name": "Iron",
    "apollographql-client-version": "2022.10.23.01",
    "app-platform": "Iron",
    "app-version": "2022.10.23.01",
    "content-type": "application/json",
    "origin": "https://stockx.com",
    "referer": "https://stockx.com/",
    "sec-ch-ua":'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "selected-country": "US",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "x-abtest-ids": "ab_alipay_hk_promo_web.control,ab_australia_address_city_label_web.true,ab_browse_search_graphql_web.true,ab_chk_entry_optimization_web_v1.true,ab_chk_great_value_badge_web_v1.variant,ab_chk_order_status_reskin_web_v3.true,ab_chk_place_order_verbage_web.true,ab_chk_selling_fast_badge_web.variant,ab_chk_selling_fast_badge_web_v2.variant,ab_chk_trust_badge_web_v1.variant,ab_cs_seller_shipping_extension_web.variant,ab_desktop_home_hero_section_web.control,ab_germany_returns_expansion_web.variant,ab_germany_returns_uk_expansion_web.variant,ab_home_carousel_current_asks_bids_web.true,ab_home_pdp_recently_viewed_anonymous_web.variant,ab_home_recommended_for_you_GNN_model_web.control,ab_kakaopay_promo_web.control,ab_localized_search_mvp_web.neither,ab_merchandising_module_pdp_web.variant_2,ab_message_center_web.true,ab_pdp_all_in_bids_asks_tables_web.false,ab_pdp_increased_product_image_size_v2_desktop_web.variant,ab_pdp_remove_purchased_from_related_web.false,ab_pdp_zoom_on_product_photo_web.control,ab_pirate_most_popular_around_you_module_web.neither,ab_pirate_product_page_dlp_gshop_v3_web.variant_1,ab_pirate_product_page_dlp_intl_retest_web.neither,ab_search_static_ranking_v1_web.control,ab_sell_flow_refactor_web_v2.true,ab_web_aa_continuous.false",
    "x-stockx-device-id": "28e9059b-3395-46a2-9813-e97ddd7662d1"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.json())