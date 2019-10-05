# pytorch-image-classification
pytorch를 이용해 이미지를 남자, 여자로 분류하며 image classification에 대해 배운다. 각 모델 별로 학습해본다.

1. 웹크롤링을 통해 이미지를 수집한다. 수집한 이미지 중 학습에 적합한 이미지들을 추려 가공한다.
+ python 3.7.3
  + [cv2 4.1.1](https://opencv.org/)  
  + [google_images_download](https://google-images-download.readthedocs.io/en/latest/index.html)

    * google_images_download에서 100장보다 더 많은 수의 이미지를 한 번에 다운로드하는 방법  
      
      Chrome과 동일한 버전의 Chromedriver가 필요하다. Chrome의 버전은 설정 - Chrome 에서 확인할 수 있다.  
      만약 Chrome이 설치되어 있지 않다면 Chrome은 아래에서 받을 수 있다.  
      https://www.google.com/intl/ko/chrome/  
      Chromedriver는 아래에서 받을 수 있다.  
      https://chromedriver.chromium.org/downloads  
  
      arguments 에 다음을 추가한다.
      "chromedriver":"path"
      
      e.g.
      ```python  
      arguments = {"keywords":keywords, "chromedriver":"c:/path/to/chromedriver.exe}  
      ```  

2. Google Colaboratory 에서 수집한 이미지들을 각 model 별로 학습시키고 비교해본다.
  + python 3.6.8
    + torch 1.1.0

## result

test1 : 학습된 이미지와 유사한 이미지들로 구성되었다.  
test2 : 학습된 이미지와 표정, 각도 등에 차이가 있는 이미지들로 구성되었다.  

![mlp](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/mlp.png)
![mlp2](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/mlp2.png)  
![cnn](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/cnn.png)
![vgg](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/vgg.png)
![resnet](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/resnet.png)  

ReLu vs Sigmoid  
![mlprelusig](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/mlprelusig.png)  

모델별 비교  

![mlpcnnvggresnet](https://github.com/KimHS0915/pytorch-image-classification/blob/master/img/mlpcnnvggresnet.png)  

| Accuracy | test1 | test2 |
|:----|:-----:|------:|
| MLP |  90% | 71%  |
| MLP(Sigmoid) | 50% | 50% |
| CNN |  92% | 80% |
| VGG |  91% | 81% |
| RESNET | 94% | 79% |



