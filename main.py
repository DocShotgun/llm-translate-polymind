import requests

# Define constants
MAX_TOKENS = 250


def main(params, memory, infer, ip, Shared_vars):
    # Definitions for API-based translation
    API_ENDPOINT_URL = Shared_vars.API_ENDPOINT_URI
    if Shared_vars.TABBY:
        API_ENDPOINT_URL += "v1/completions"
    else:
        API_ENDPOINT_URL += "completion"

    def infer(prompt):
        payload = {
            "prompt": prompt,
            "model": "gpt-3.5-turbo-instruct",
            "max_tokens": MAX_TOKENS,
            "n_predict": MAX_TOKENS,
            "stream": False,
            "seed": -1,
            "top_k": 1,
            "stop": "::END TEXT::",
        }
        request = requests.post(
            API_ENDPOINT_URL,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Shared_vars.API_KEY}",
            },
            json=payload,
            stream=False,
            timeout=360,
        )
        return request.json().get("choices")[0].get("text")

    # Create translation prompt
    prompt = f"""::JAPANESE TEXT::
1月下旬、大手カレーチェーン「カレーハウスCoCo (ココ）壱(いち)番屋」のキッチンカーがやってきたのは、24人が避難する石川県七尾市の能登島地区コミュニティセンターだ。量や辛さの希望を社員が聞き取り、ご飯をよそった容器のふたの上に温かいレトルトパウチを載せて渡す。
::END TEXT::
::ENGLISH TEXT::
In late January, the kitchen car from the major curry chain "Curry House CoCo Ichibanya" arrived at a community center in the Notojima area of Nanao City, Ishikawa Prefecture, where 24 people were taking shelter. The staff took orders for the desired amount and spiciness of the curry, then served it by placing a warm retort pouch on top of a lid covering a container filled with rice.
::END TEXT::
***
::ENGLISH TEXT::
Austria is a country south of Germany which is often confused with Australia by English speakers. All the same, we only have kangaroos in zoos.
::END TEXT::
::GERMAN TEXT::
Österreich ist ein Land südlich von Deutschland, das von Englisch-Sprechern gerne mit Australien verwechselt wird. Dennoch gibt es bei uns Kängurus nur in Tiergärten.
::END TEXT::
***
::{params.get("source_lang").upper()} TEXT::
{params.get("text")}
::END TEXT::
::{params.get("target_lang").upper()} TEXT::"""

    response = infer(prompt)
    translation = response.split(f'::{params.get("target_lang").upper()} TEXT::')[
        -1
    ].strip()

    # Handle unsuccessful search
    if len(translation) == 0:
        print("No translation results")
        return "No translation results received, please translate to the best of your ability"

    print(translation)
    return "<translation_results>:\n" + translation + "</translation_results>"


if __name__ == "__main__":
    main(params, memory, infer, ip, Shared_vars)
