### all, 8 버전의 경우 판다스 변환과정 중 오류 발생 -> 수정 중

* Rhytm wave 5000으로 통일
* data shuffle 기능 추가
* all, only-2, 8 version 추가  
 
  
version 설명  
  
**1. lead 2 only**  
Rhythm waveform 중 lead 2, 즉 II 만 사용  

　구조:  
　　data = {  
  　　　'Subject' = [ ],  
  　　　'Lead2' = [(데이터 길이: 5000)],  
  　　　'Label' = [0: normal, 1: arrythmia].  
　　}
  
**2. all**  
Median, Rhythm waveform의 모든 lead 사용  

　구조:  
　　data = {  
  　　　'Subject' = [ ],  
  　　　'Lead' = {  
     　　　　'Median' = {'여러 lead' = (데이터)},  
     　　　　'Rhythm' = {'여러 lead' = (데이터)}  
        　　　},  
  　　　'Label' = [0: normal, 1: arrythmia].  
　　}
  
**3. 8**  
Rhythm waveform 중 통일되는 8가지 lead 사용

　구조:  
　　data = {  
  　　　'Subject' = [ ],  
  　　　'Lead' = [데이터 shape: 8 x 5000],  
  　　　'Label' = [0: normal, 1: arrythmia].  
　　}

