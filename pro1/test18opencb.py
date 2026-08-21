# #Computer Vision(opencv:Open Source Computer Vision 라이브러리 사용)

# #pip install opencv-python
# #conda install opencv-python
# import cv2
# print(cv2.__version__)

# img1 = cv2.imread('test18ani.jpg')
# print(type(img1)) #<class 'numpy.ndarray'>

# cv2.imshow('image test',img1)
# cv2.waitKey()
# cv2.destroyAllWindows()
# # print('end')

# #다름 이름으로 저장
# # cv2.imwrite('test18ani2.jpg',img1)
# # cv2.imwrite('test18ani3.jpg', img1, [cv2.IMWRITE_JPEG_QUALITY, 1])



# # 맞음 - 파일명 문자열과 img2 변수가 별개의 인자로 구분됨
# cv2.imwrite('test18ani14.jpg', img1,[cv2.IMWRITE_JPEG_QUALITY, 1])


# #이미지 크기 조정
# img2 = cv2.resize(img1,(300,100),interpolation=cv2.INTER_AREA)
# cv2.imwrite('test18ani14.jpg,img2')

# #밝기,상화좌우 회전, 자르기

