# eia_crawler

主要工作是將環保署及各縣市環保局歷年受理審查之環境影響評估書件資料收集成 CSV 格式檔案。

資料來源：[行政院環境保護署 環評書件查詢系統](http://eiareport.epa.gov.tw/EIAWEB/Main.aspx?func=00)

## 安裝

+  Scrapy 套件 (可參考 [Scrapy Document - Installation guide](http://doc.scrapy.org/en/latest/intro/install.html))

## Vagrant

若是想用 Vagrant 也可以參考Gist上的 [Vagrant File](https://gist.github.com/dz1984/11130582)。

## 使用方式

分為兩個步驟：
+ Report -  將各分頁清單抓下來，目的是要得到環評書件案號。

+ Detail -  從清單中的案號，取得更詳細欄位。

``` bash
$ scrapy crawl report

$ scrapy crawl detail
```

## 產出結果

+ [results/list/result.csv](results/list/result.csv)

``` csv
EXTP,DST,EDN,DOCTYPE,PER,HCODE,NOTES

審查進度,環評機關,名稱,類別,承辦人,案號,說明
```

+ [results/detail/result.csv](results/detail/result.csv)

``` csv
HCODE,DOCTYP,TAKER,DST,TRIA,DIRORG,DECAL,DSUNT,NOTES,SEDAT,EXTP,DEPN,COMIT,DSIZE,PORCS,DAREA

案號,書件類別,承辨人,基地行政區,初審會日期,目的事業主管機關,開發計畫類別,,備註,繳費日期,審查結論別,開發單位名稱,委員會日期,開發規模,處理情形,基地面積
```

## License 

The MIT license (MIT)
