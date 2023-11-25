from openai import OpenAI
import json
import yaml

with open("secret.yaml") as file:
  secret = yaml.safe_load(file)
api_key = secret["openai_api_key"]

client = OpenAI(api_key=api_key)

def load_articles(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def generate_summary(article, max_tokens=350):
    prompt = f"Summarize this article into a concise script for a video of around 60 seconds (approximately 125 words). Do not include anything else in your response except the summarised text:\n\n{article['content']}"

    # response = client.completions.create(model="gpt-4-1106-preview",
    # prompt=prompt,
    # max_tokens=max_tokens,
    # temperature=0.7)
    # return response.choices[0].text.strip()

    completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "You are a journalist, skilled in summarising news articles concisely."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=max_tokens
    )

    return completion.choices[0].message.content

def save_articles_with_summaries(articles_with_summaries, filename):
    with open(filename, 'w') as file:
        json.dump(articles_with_summaries, file, indent=4)

def main():
    articles = load_articles('./mrdn_scraper/articles.json')
    video_scripts = []

    for article in articles:
        summary = generate_summary(article)
        video_scripts.append({
            'title': article['title'],
            'video_script': summary
        })
        article['video_script_summary'] = summary

    # Print or save the video scripts
    for script in video_scripts:
        print(f"Title: {script['title']}\nScript: {script['video_script']}\n\n")

    save_articles_with_summaries(articles, 'articles_with_summaries.json')
    print("Saved articles with summaries to 'articles_with_summaries.json'.")

if __name__ == "__main__":
    main()
