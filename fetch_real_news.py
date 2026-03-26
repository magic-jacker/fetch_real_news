#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fetch_cls_telegraph():
    url = "https://www.cls.cn/telegraph"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('.telegraph-content a')[:10]
        return [{'title': i.get_text(strip=True), 'url': 'https://www.cls.cn' + i.get('href', ''), 'source': '财联社电报', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')} for i in items if len(i.get_text(strip=True)) > 10][:6]
    except: return []

def fetch_cls_finance():
    url = "https://www.cls.cn/finance"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('a[href*="/detail/"]')[:8]
        return [{'title': i.get_text(strip=True), 'url': 'https://www.cls.cn' + i.get('href', ''), 'source': '财联社财经', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')} for i in items if len(i.get_text(strip=True)) > 10][:5]
    except: return []

def fetch_36kr():
    url = "https://36kr.com/information/web_news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('a[href*="/p/"]')[:10]
        news = []
        for i in items:
            t = i.get_text(strip=True)
            if len(t) > 10 and not any(w in t for w in ['广告', '推广', '直播']):
                news.append({'title': t, 'url': 'https://36kr.com' + i.get('href', ''), 'source': '36氪', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
        return news[:5]
    except: return []

def fetch_tmtpost():
    url = "https://www.tmtpost.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('h3 a, h2 a')[:8]
        return [{'title': i.get_text(strip=True), 'url': 'https://www.tmtpost.com' + i.get('href', ''), 'source': '钛媒体', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')} for i in items if len(i.get_text(strip=True)) > 10][:4]
    except: return []

def fetch_huxiu():
    url = "https://www.huxiu.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('a[href*="/article/"]')[:8]
        return [{'title': i.get_text(strip=True), 'url': 'https://www.huxiu.com' + i.get('href', ''), 'source': '虎嗅', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')} for i in items if len(i.get_text(strip=True)) > 10 and not any(w in i.get_text(strip=True) for w in ['广告', '推广'])][:4]
    except: return []

def fetch_wallstreetcn():
    url = "https://wallstreetcn.com/articles"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('h2 a, h3 a')[:8]
        return [{'title': i.get_text(strip=True), 'url': 'https://wallstreetcn.com' + i.get('href', ''), 'source': '华尔街见闻', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')} for i in items if len(i.get_text(strip=True)) > 10][:4]
    except: return []

def categorize_news(news_list):
    categories = {'finance': [], 'industry': [], 'tech': [], 'byd': [], 'tencent': [], 'fitness': [], 'other': []}
    keywords = {
        'finance': ['央行', 'LPR', '北向资金', '南向资金', '外资', 'A股', '港股', '美股', '上证指数', '基金', '债券', 'IPO', '证监会', '银保监会', '交易所', '降准', '降息', '汇率', '黄金', '原油'],
        'industry': ['新能源', '电动车', '锂电池', '储能', '光伏', '风电', '氢能源', '半导体', '芯片', '集成电路', '机器人', '智能制造', '手机', 'PC', 'AR', 'VR', '汽车销量', '医药', '生物医药', 'CXO'],
        'tech': ['AI', '人工智能', '大模型', 'ChatGPT', 'GPT', '生成式AI', 'AIGC', '苹果', 'iPhone', '华为', 'Mate', '鸿蒙', '小米', '谷歌', 'Gemini', '微软', 'Meta', '英伟达', 'NVIDIA', 'GPU', 'OpenAI', '特斯拉', '阿里巴巴', '阿里云', '腾讯', '百度', '字节跳动', '抖音', '5G', '6G', '云计算', '区块链', 'Web3', 'NFT'],
        'byd': ['比亚迪', 'BYD', '王传福', '刀片电池', 'DM-i', '仰望', 'U8', '腾势', '海豹', '海豚', '汉', '唐', '护卫舰07', '驱逐舰05','第二代刀片电池','兆瓦闪充2.0','闪充技术','全域1000V高压平台','1500kW超充功率','10C充电倍率','零下30度闪充','DM-i 6.0','天神之眼5.0','DiPilot 5.0','宋Ultra EV','海豹07 EV','腾势Z9 GT','仰望U7','20000座闪充站','T型滑轨闪充桩','油电同速','闪充中国战略'],
        'tencent': ['腾讯', 'Tencent', '马化腾', '微信', 'QQ', '王者荣耀', '和平精英', '元梦之星', '腾讯云', '腾讯音乐', '腾讯视频', '阅文集团', '元宝', '混元大模型'],
        'fitness': ['健身', '增肌', '减脂', '减肥', '力量训练', '有氧运动', '蛋白质', '健身房', '跑步', '马拉松', '游泳', '深蹲', '硬拉', '卧推', '肌酸']
    }
    for news in news_list:
        for cat, words in keywords.items():
            if any(word in news['title'] for word in words):
                categories[cat].append(news)
                break
        else:
            categories['other'].append(news)
    return categories

def main():
    all_news = fetch_cls_telegraph() + fetch_cls_finance() + fetch_36kr() + fetch_tmtpost() + fetch_huxiu() + fetch_wallstreetcn()
    unique = []
    seen = set()
    for n in all_news:
        if n['title'] not in seen:
            seen.add(n['title'])
            unique.append(n)
    result = {
        'timestamp': datetime.now().isoformat(),
        'total': len(unique),
        'sources': {'财联社电报': len(fetch_cls_telegraph()), '财联社财经': len(fetch_cls_finance()), '36氪': len(fetch_36kr()), '钛媒体': len(fetch_tmtpost()), '虎嗅': len(fetch_huxiu()), '华尔街见闻': len(fetch_wallstreetcn())},
        'categories': categorize_news(unique),
        'raw_news': unique
    }
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
