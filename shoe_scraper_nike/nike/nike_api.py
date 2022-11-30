import requests
from pprint import pprint


def api_call():
    
    """
        Anchor in the query string acts as the prev and next page argument. It runs in inrecements of 24 modify that and you can 
        get new shoes.   
    """
    url = "https://api.nike.com/cic/browse/v2"

    querystring = {"queryid":"products","anonymousId":"961799892A2BB4DCC74C4104F0FF75DE","country":"us","endpoint":"/product_feed/rollup_threads/v2?filter=marketplace(US)&filter=language(en)&filter=employeePrice(true)&filter=attributeIds(16633190-45e5-4830-a068-232ac7aea82c)&anchor=120&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24","language":"en","localizedRangeStr":"{lowestPrice} — {highestPrice}"}

    payload = ""
    headers = {
        "cookie": 'optimizelyEndUserId=oeu1666476076518r0.5324603464788851; s_ecid=MCMID%7C66716223770298801846096233966282075827; AMCV_F0935E09512D2C270A490D4D%40AdobeOrg=1994364360%7CMCMID%7C66716223770298801846096233966282075827%7CMCAID%7CNONE%7CMCOPTOUT-1666483276s%7CNONE%7CvVersion%7C3.4.0; guidS=0ae6fedb-8fc5-48d5-dc7e-ee92a7bbaaf0; guidU=addbd812-7e56-4732-db6c-38259be76ecc; anonymousId=961799892A2BB4DCC74C4104F0FF75DE; _gcl_au=1.1.2004213928.1666476093; _scid=bb649212-e825-45f5-8a4d-b7d30112f199; AnalysisUserId=23.62.45.14.282651666479007307; cid=undefined%7Cundefined; RES_TRACKINGID=69289428741097466; ResonanceSegment=1; pixlee_analytics_cookie=%7B%22CURRENT_PIXLEE_USER_ID%22%3A%2289a3e8f5-a7bb-7dd5-3343-468de9fb34b4%22%7D; pixlee_analytics_cookie_legacy=%7B%22CURRENT_PIXLEE_USER_ID%22%3A%2289a3e8f5-a7bb-7dd5-3343-468de9fb34b4%22%7D; NIKE_COMMERCE_COUNTRY=US; NIKE_COMMERCE_LANG_LOCALE=en_us; CONSUMERCHOICE=US/en_us; QUALTRICS_LANGUAGE=EN; _sp_id.759a=a33b4613-33ae-4c13-ab00-518124c958a6.1666722556.1.1666722556.1666722556.90874c52-dfa0-4d9a-99c4-b813f85afeed; _ga_S6TK03XKR2=GS1.1.1666722554.1.1.1666722587.0.0.0; _tt_enable_cookie=1; _ttp=9a0ef49d-1851-4439-813b-e2e105667272; geoloc=cc=US,rc=CA,tp=vhigh,tz=PST,la=37.3519,lo=-121.952; feature_enabled__as_nav_rollout=true; audience_segmentation_performed=true; bm_sz=1E2A1379E85E88593A490051303AE9DB~YAAQvzLFF73obf+DAQAA6zgNMREDLscabF8L0tjwgjpapNaedZqWlSjP9IC79s4Np7Zo5BCc96qE+UNPM9lZZYfrU1HfwKD4NznZFEqGeiE0RpmviwrCk2bTL/aRrbBPIbHjSRfUCD0qTRMP+r+BLuyAstPyImL4zH2vDe665LS/SLkrXW4g6QwR8uY766QBjn+t5eDJD2HUQ7Tuk9IifgzzAVCFkN3RTDrejRjE+f5DRMHJsmvW0fO6Hj9Lktvhwy+DDTShuFYNhSGo/fVthCSO2a6rZ7Jc0BexuPvvR9Fh39r2mtOhNE6F+69RJ42r9yoUQwL4mb+sYmM2qGBNLWx6gRt44xQcBcfQkGnPIy/6pIfqG3hSyajtDcoLS1RHfyWTpf7JsZzK3hic390lpHDC~4600112~3683641; ak_bmsc=E6E152AC0E1C5C64AC94996E7927B3C4~000000000000000000000000000000~YAAQvzLFF+3obf+DAQAA0kENMREeVkE3SDS/hTPkE9TsN0b81JzCLalkY0Racwjti1ZRStvgteGySpPwvKqg5b/X8b/ZdsKirZEF9C9bKYe65U7e5cnCbodqwPO/g9iZQE+fRSGXfcuQ4PH/nnH1vacYehHRW2sPV9PvPPpwjAezAMoLcYbIkXCNPn4HxZY7MmsDsdstBrCkORCnQhSSZs6z11JXKtx5hdejYVLW/dV5UQ+2Tn2WCiSQlZHFHh55lC79yGkWPhfDTCg8DekLD8SLzQuGvTpIebiFj0KRSXHQxvm7VGV514DLeFmmj8AsiAqvrLRnqDxU5cWaYErLwNuUUGt42sI7XyuAnbhctoQVaZ0XSvWmpmUq2tzc1u7a/LB74rI6Dgc8jFehRyMEuhaqGqO2Zg8XA0votEFGcnrNCUA8aNk5vYZFWURLl3aA7mz7RqVw9XBiIXyyxlfP+5hDvgQ6qGqzoCY9/VUrIuomsWE+Ui4qQ7I=; _gid=GA1.2.68683053.1667270269; ppd=pw|nikecom>pw>shoes; AKA_A2=A; ak_bmsc_nke-2.2-ssn=0SQQSTajdxVYbPzPQo96M09WlZuUGDcV4uvUmGRf59KqbuDfe1zWe2tTu5yhoOrxXhZbMS0bldgNLh6OA9PyCIKqbepOgSq4Ly2cwpYGKKxLPvRezdvyl20Eh8jSDnrnvcsyPb68Gun2mwm5ltQnVAW0N; ak_bmsc_nke-2.2=0SQQSTajdxVYbPzPQo96M09WlZuUGDcV4uvUmGRf59KqbuDfe1zWe2tTu5yhoOrxXhZbMS0bldgNLh6OA9PyCIKqbepOgSq4Ly2cwpYGKKxLPvRezdvyl20Eh8jSDnrnvcsyPb68Gun2mwm5ltQnVAW0N; RT="z=1&dm=nike.com&si=d2890b49-873b-4f7f-925e-a2f16da5aa7e&ss=l9xn2cwh&sl=2&tt=857&bcn=%2F%2F17de4c11.akstat.io%2F&ld=12gzz"; bm_sv=08524D8B8E27E65B080822B2D203A0D4~YAAQ3DLFF0AMiNSDAQAAV4BMMRF6/GUjhn2O+leES6dNN7VLTxmNwYJ9R71+vaTSw8mONh9w/n7RAi48BY4DtAJ6DCH8VC54F/5gwO6dT8SrSMNN+x+BU96gR0mjlxdJAwf7cQDZHDzRRXIk79C0R/A0SWmNQ3fTVtkVM2Bwe2lEcOLimsyHvjHl+ZGlt/jCYzzx2IYrGnDzv1lhFXEs+s6TqJCddKKTr/5g+ZhzLU7g3LRut2TS5Xep8coyjuI=~1; bc_nike_triggermail=%7B%22distinct_id%22%3A%20%221831671272198d-00e21ec62a4681-1b525635-13c680-1831671272211e4%22%2C%22bc_persist_updated%22%3A%201666476093564%2C%22cart_total%22%3A%200%7D; _ga=GA1.2.21000866.1666476093; cto_bundle=sdixyl9TMHcwZGdkbXlBcVNpWldhZ3pxM0RoZ0l2MGVxaGhaU1dmQ3glMkZjWktQZDl4TElzSnZBUkdRUFpYRjlXVkVYc3ljODZ6UTVOSzJuYkNhWWI1QnZheVF2TzNrRU1uJTJGb0l5M244Mjlib1JaelZKOFhhazUxQ1YzeDBMdXJyUk13RjNEcXFZWmc5YyUyRm5Kc2Z6T0hjV1Q2YmVpS2Y0cjVNYXJsS0g1Y2hXNFN1ODE2VkpocFhiJTJGUVVnTWNpem8zMGZUVg; _ga_QTVTHYLBQS=GS1.1.1667272612.18.1.1667274640.60.0.0; _abck=82F9380612EA60649DFF12FA7A0EAA7F~-1~YAAQBTPFF2aFmSOEAQAAjL9QMQjjElou2wlZekgsij4qObTIk1ekGSlcrCNXVQcKnJwfS/m3qRdPgMNZeaAEPSqAToLYGe8/LXvtPuHrQdrgltViJukVzwRJ3ErDZe2eSwXI23B8WvgTh5F5L1Cmg1i4T2tljlsgZLI3JhXdqYS3c2jLN3IKA2y8vSrV/EjBLrWoocUBkoxZYgnNRnEYCkfsq08ipVrQ+QRs377QcYKnp5ZxkZj4KT4MrMBLrHiaiDjLJzUsSJ3LCzw3i29o8V+HL3LCpY+6yLDtWlXIX7b5fGgH6iS51kyvnBN1ErCWF/750k8LMI/IIG2WKeCapJsQ4T5ekF53NUGXOd5p/W4vo7jVXEweZcNXGKCv+ZI6eIYoHOpnvg+Zq1XENto+nE7/D3q/VVm1l6Xi1MmeG+2zg1RoCFXKcrZk0FCnKOkDAtRV9hH2BEFp2BgBk6JdEZ6egmvm+xs/ssm7IWRyIcnCLuMJIVs1i48tHCqg/kRcC0WCmHfob5m++GC/5OXTuNlR/aXA~-1~-1~-1',
        "authority": "api.nike.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.nike.com",
        "referer": "https://www.nike.com/",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    increment = 24
    still_more_shoes = True
    shoe_info = []
    try:
        while still_more_shoes:
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code != 200:
                still_more_shoes = False
                break
            data = response.json().get("data").get("products").get("products")
            for datem in data:
                shoe = {}
                #price = datem.get("price").get("currentPrice")
                for color in datem.get("colorways"):
                    get_link = color.get("pdpUrl").replace("{countryLang}","")
                    #link = f"https://www.nike.com{get_link}"
                    title = color.get("pdpUrl").replace("{countryLang}/t/","")
                    title_arr = title.split("/")
                    title = title_arr[0]
                    # What if you come accress slides?
                    if "shoes" in title:
                        index = title.index("shoes")
                        title = title.replace(title[index:],"shoes")
                    break
                shoe["title"] = title
                # shoe["price"] = price
                # shoe["link"] = link    
                shoe_info.append(shoe)
            print(f"{len(shoe_info)} shoes found.") 
            # Modify anchor in query string
            increment = increment+24
            querystring["endpoint"] = f"/product_feed/rollup_threads/v2?filter=marketplace(US)&filter=language(en)&filter=employeePrice(true)&filter=attributeIds(16633190-45e5-4830-a068-232ac7aea82c)&anchor={increment}&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24"
    except Exception as e:
        print(f"error: {e}")
    return shoe_info
            
    
print(api_call())