# pytorch-image-classification
pytorch를 이용해 이미지를 남자, 여자로 분류하며 image classification에 대해 배운다. 각 모델 별로 학습해본다.

1. 웹크롤링을 통해 이미지를 수집한다. 수집한 이미지 중 학습에 적합한 이미지들을 추려 가공한다.
+ python 3.7.3
  + [cv2 4.1.1](https://opencv.org/)  
  + [google_images_download](https://google-images-download.readthedocs.io/en/latest/index.html)

2. Google Colaboratory 에서 수집한 이미지들을 각 model 별로 학습시키고 비교해본다.
  + python 3.6.8
    + torch 1.1.0

## result
모델 별 정확도  

|     | test1 | test2 |
|:----|:-----:|------:|
| MLP |  0.92 | 0.72  |
| MLP(Sigmoid) | 0.5 | 0.5 |
| CNN |  0.92 | 0.79 |
| VGG |  0.93 | 0.86 |
| RESNET | 0.92 | 0.8 |

test1 : 학습된 이미지와 유사한 이미지들로 구성되었다.  
test2 : 학습된 이미지와 표정, 각도 등에 차이가 있는 이미지들로 구성되었다.
