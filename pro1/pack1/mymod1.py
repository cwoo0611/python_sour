#pack1/mymod1.py
#변수,함수를 갖음(다른 모듈에서 사용하기 위함). 실행은 x 
tot = 123

def lstHap(*ar):
    print(ar)
    if __name__ == ' __main__':
        print('나는 메인 모듈이야')

def kbsFunc():
    print('대한민국 대표방송')

def mbcFunc():
    print('문화방송')
    