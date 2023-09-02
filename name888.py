from fastapi import FastAPI, File, UploadFile
import os
import json
import torch

app = FastAPI()

def transcribe_audio(file: UploadFile = File(...)):
    def process_audio(file):
        filename = file.filename
        content = file.read()  # 读取上传的音频文件内容
        result = model.transcribe(content, word_timestamps=True, **transcribe_options)
        segments = result["segments"]
        lang = result['language']
        if lang not in list(lang2token.keys()):
            print(f"{lang} not supported, ignoring...\n")
            return {"error": f"{lang} not supported."}
        character_name = filename.rstrip(".wav").split("")[0]
        code = filename.rstrip(".wav").split("")[1]
        if not os.path.exists(f"./segmented_character_voice/{character_name}"):
            os.makedirs(f"./segmented_character_voice/{character_name}")
        wav, sr = torchaudio.load(content)  # 使用上传的音频文件内容加载音频数据
        # Do the necessary audio processing steps with `wav` and `sr`.
        # ...
        # Return the transcribed text as a response.
        return {"text": "Transcribed text here."}

    return process_audio(file)

def main():
    parent_dir = "./denoised_audio/"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    filelist = list(os.walk(parent_dir))[0][2] if os.path.exists(parent_dir) else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="CJE")
    parser.add_argument("--whisper_size", default="medium")
    args = parser.parse_args()
    if args.languages == "CJE":
        lang2token = {
            'zh': "[ZH]",
            'ja': "[JA]",
            "en": "[EN]",
        }
    elif args.languages == "CJ":
        lang2token = {
            'zh': "[ZH]",
            'ja': "[JA]",
        }
    elif args.languages == "C":
        lang2token = {
            'zh': "[ZH]",
        }
    assert torch.cuda.is_available(), "Please enable GPU in order to run Whisper!"
    with open("./configs/finetune_speaker.json", 'r', encoding='utf-8') as f:
        hps = json.load(f)
    target_sr = hps['data']['sampling_rate']
    model = whisper.load_model(args.whisper_size)
    for file in filelist:
        print(f"transcribing {parent_dir + file}...")
        result = transcribe_audio(parent_dir + file)
        print(result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)