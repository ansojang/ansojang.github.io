#!/usr/bin/env python3
# 그리드센서 데이터 자동 최신화 (GitHub Actions에서 매주 수요일 자정 KST 실행)
# 주식=야후파이낸스, 코인=업비트(원화). 종목별 실패 시 기존 데이터 유지.
import json, time, datetime, urllib.request, urllib.parse, os

HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"prices.json")
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Accept":"application/json"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=40).read()

STOCKS=[['005930.KS', '삼성전자', 'KR'], ['000660.KS', 'SK하이닉스', 'KR'], ['005380.KS', '현대차', 'KR'], ['009150.KS', '삼성전기', 'KR'], ['373220.KS', 'LG에너지솔루션', 'KR'], ['207940.KS', '삼성바이오로직스', 'KR'], ['028260.KS', '삼성물산', 'KR'], ['032830.KS', '삼성생명', 'KR'], ['105560.KS', 'KB금융', 'KR'], ['012450.KS', '한화에어로스페이스', 'KR'], ['000270.KS', '기아', 'KR'], ['055550.KS', '신한지주', 'KR'], ['329180.KS', 'HD현대중공업', 'KR'], ['034020.KS', '두산에너빌리티', 'KR'], ['012330.KS', '현대모비스', 'KR'], ['068270.KS', '셀트리온', 'KR'], ['006400.KS', '삼성SDI', 'KR'], ['066570.KS', 'LG전자', 'KR'], ['086790.KS', '하나금융지주', 'KR'], ['035420.KS', 'NAVER', 'KR'], ['000810.KS', '삼성화재', 'KR'], ['267260.KS', 'HD현대일렉트릭', 'KR'], ['042660.KS', '한화오션', 'KR'], ['010130.KS', '고려아연', 'KR'], ['005490.KS', 'POSCO홀딩스', 'KR'], ['316140.KS', '우리금융지주', 'KR'], ['017670.KS', 'SK텔레콤', 'KR'], ['096770.KS', 'SK이노베이션', 'KR'], ['011200.KS', 'HMM', 'KR'], ['051910.KS', 'LG화학', 'KR'], ['NVDA', '엔비디아', 'US'], ['AAPL', '애플', 'US'], ['GOOGL', '알파벳(구글)', 'US'], ['MSFT', '마이크로소프트', 'US'], ['AMZN', '아마존', 'US'], ['AVGO', '브로드컴', 'US'], ['TSLA', '테슬라', 'US'], ['META', '메타', 'US'], ['LLY', '일라이릴리', 'US'], ['BRK-B', '버크셔해서웨이', 'US'], ['JPM', 'JP모건', 'US'], ['WMT', '월마트', 'US'], ['AMD', 'AMD', 'US'], ['V', '비자', 'US'], ['XOM', '엑슨모빌', 'US'], ['JNJ', '존슨앤드존슨', 'US'], ['MA', '마스터카드', 'US'], ['INTC', '인텔', 'US'], ['ABBV', '애브비', 'US'], ['CSCO', '시스코', 'US'], ['PLTR', '팔란티어', 'US'], ['BAC', '뱅크오브아메리카', 'US'], ['ORCL', '오라클', 'US'], ['COST', '코스트코', 'US'], ['CVX', '셰브론', 'US'], ['KO', '코카콜라', 'US'], ['AMAT', '어플라이드머티어리얼즈', 'US'], ['MRK', '머크', 'US'], ['GE', 'GE에어로스페이스', 'US'], ['UNH', '유나이티드헬스', 'US']]
COINS=[['KRW-BTC', '비트코인'], ['KRW-ETH', '이더리움'], ['KRW-XRP', '엑스알피(리플)'], ['KRW-DOGE', '도지코인'], ['KRW-USDT', '테더']]

# ---------- 야후(주식) ----------
def yahoo_block(sym,rng,intv,mkt):
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={intv}"
    res=json.loads(get(url))["chart"]["result"][0]
    ts=res.get("timestamp") or []; q=res["indicators"]["quote"][0]
    hh,hl,hc=q["high"],q["low"],q["close"]
    d,n,H_,L_,C_=[],[],[],[],[]; cur,cnt=None,0
    for i,t in enumerate(ts):
        c=hc[i]; hi=hh[i]; lo=hl[i]
        if c is None or hi is None or lo is None: continue
        lt=time.gmtime(t); day=lt.tm_year*10000+lt.tm_mon*100+lt.tm_mday
        if day!=cur:
            if cur is not None: d.append(cur); n.append(cnt)
            cur=day; cnt=0
        r=1 if mkt=="KR" else 2
        H_.append(round(hi,r)); L_.append(round(lo,r)); C_.append(round(c,r)); cnt+=1
    if cur is not None: d.append(cur); n.append(cnt)
    return {"d":d,"n":n,"h":H_,"l":L_,"c":C_}

def yahoo_ticker(sym,name,mkt):
    return {"name":name,"mkt":mkt,"res":{
        "1h":yahoo_block(sym,"260d","1h",mkt),
        "5m":yahoo_block(sym,"60d","5m",mkt),
        "1m":yahoo_block(sym,"7d","1m",mkt)}}

# ---------- 업비트(코인) ----------
def rnd(p): return round(p) if p>=100 else round(p,4)
def upbit_block(market,unit,days):
    start=datetime.datetime.utcnow()-datetime.timedelta(days=days); seen={}; to=None
    while True:
        url=f"https://api.upbit.com/v1/candles/minutes/{unit}?market={market}&count=200"
        if to: url+="&to="+urllib.parse.quote(to)
        batch=None
        for a in range(4):
            try: batch=json.loads(get(url)); break
            except Exception: time.sleep(1.5)
        if not batch: break
        for x in batch: seen[x["candle_date_time_utc"]]=x
        o=batch[-1]["candle_date_time_utc"]
        if datetime.datetime.strptime(o,"%Y-%m-%dT%H:%M:%S")<=start: break
        to=o; time.sleep(0.05)
    rows=sorted(seen.values(),key=lambda x:x["candle_date_time_utc"])
    rows=[x for x in rows if datetime.datetime.strptime(x["candle_date_time_utc"],"%Y-%m-%dT%H:%M:%S")>=start]
    d,n,H_,L_,C_=[],[],[],[],[]; cur,cnt=None,0
    for x in rows:
        k=x["candle_date_time_kst"]; day=int(k[0:4])*10000+int(k[5:7])*100+int(k[8:10])
        if day!=cur:
            if cur is not None: d.append(cur); n.append(cnt)
            cur=day; cnt=0
        H_.append(rnd(x["high_price"])); L_.append(rnd(x["low_price"])); C_.append(rnd(x["trade_price"])); cnt+=1
    if cur is not None: d.append(cur); n.append(cnt)
    return {"d":d,"n":n,"h":H_,"l":L_,"c":C_}

def upbit_ticker(market,name):
    return {"name":name,"mkt":"COIN","res":{
        "1h":upbit_block(market,60,200),
        "5m":upbit_block(market,5,20),
        "1m":upbit_block(market,1,3)}}

# ---------- 실행 ----------
old={}
if os.path.exists(OUT):
    try: old=json.load(open(OUT))
    except Exception: old={}
out={}; ok=0; fail=0
for sym,name,mkt in STOCKS:
    try:
        out[sym]=yahoo_ticker(sym,name,mkt); ok+=1
        print("OK",sym,name,len(out[sym]["res"]["1h"]["h"]),"bars",flush=True)
    except Exception as e:
        fail+=1; print("FAIL",sym,e,flush=True)
        if sym in old: out[sym]=old[sym]   # 실패 시 기존 유지
    time.sleep(0.3)
for market,name in COINS:
    try:
        out[market]=upbit_ticker(market,name); ok+=1
        print("OK",market,name,len(out[market]["res"]["1h"]["h"]),"bars",flush=True)
    except Exception as e:
        fail+=1; print("FAIL",market,e,flush=True)
        if market in old: out[market]=old[market]
    time.sleep(0.3)

json.dump(out,open(OUT,"w"),ensure_ascii=False,separators=(",",":"))
print(f"\nDONE ok={ok} fail={fail} total={len(out)} size={os.path.getsize(OUT)/1024/1024:.2f}MB")
