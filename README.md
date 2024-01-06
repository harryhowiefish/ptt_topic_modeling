## Introduction

This tool uses Latent Dirichlet Allocation (LDA) to generate topics for any particular PTT bulletin board.

## Usage

Install ckiptagger
```
pip install -U ckiptagger[tf,gdown]
```

Download WS model:
```python
from ckiptagger import data_utils
data_utils.download_data_gdown("./") # gdrive-ckip
```
or download the models from the following mirror sites
- [iis-ckip](http://ckip.iis.sinica.edu.tw/data/ckiptagger/data.zip)
- [gdrive-ckip](https://drive.google.com/drive/folders/105IKCb88evUyLKlLondvDBoh7Dy_I1tm)
- [gdrive-jacobvsdanniel](https://drive.google.com/drive/folders/15BDjL2IaX3eYdFVzT422VwCb743Hrbi3)

Run ptt_ida.py
```
python ptt_ida.py 看版名稱 要分析的文章數量
```
## Example
```
python ptt_lda.py Boy-Girl 100
```

```
TOPIC #1 前30名詞彙
['認識', '一些', '然後', '一樣', '很多', '遇到', '興趣', '其他', '留言', '對象', '條件', '工作', '可能', '我們', '手機', '還是', '話題', '比較', '應該', '對方', '這樣', '時間', '生氣', 'pr', '照片', '生活', '問題', '交友', '軟體', '男生']


TOPIC #2 前30名詞彙
['工作', '可能', '解決', '還是', '怎麼', '態度', '根本', '時間', '認真', '出來', '時候', '建議', '只是', '事情', '然後', '感覺', '幫忙', '就是', '其實', '繼續', '所以', '別人', '不要', '喜歡', '這樣', '問題', '不會', '對方', '知道', '女友']


TOPIC #3 前30名詞彙
['不能', '比較', '的話', '然後', '在一起', '不然', '認識', '怎麼', '接受', '男生', '喜歡', '關係', '只是', '問題', '感覺', '可能', '所以', '前任', '還是', '就是', '不會', '知道', '這樣', '男友', '交往', '分手', '不要', '對方', '女友', '朋友']


TOPIC #4 前30名詞彙
['健康', '還是', '根本', '小時', '檢舉', '其實', '18', '收入', '前提', '他們', '工作', '比較', '年薪', '28', '不用', '這樣', '不會', '40', '怎麼', '30', '時間', '別人', 'ptt', '所以', '生活', '台灣', '20', '小孩', '26', '結婚']


TOPIC #5 前30名詞彙
['一下', '可能', '一樣', '生活', '上班', '就是', '怎麼', '只有', '你們', '個性', '不要', '只是', '知道', '喜歡', '所以', '這樣', '問題', '應該', '比較', '現在', '價值觀', '很多', '結婚', '老婆', '分手', '小孩', '還是', '不會', '工作', '女友']
```


## Working progress
- expand customization (set min&max_df, excluded words, )
- tools to download and load local text file without crawling everytime
- export topic labeling for documents
- test out [lda2vec](https://github.com/cemoody/lda2vec) for more in depth NLP understanding than the count vector currently used 


## Acknowledgement
- Word separation 中文斷詞 uses [ckiptagger](https://github.com/ckiplab/ckiptagger) from CKIP Lab