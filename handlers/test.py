stoimost_piva_1 = 69
stoimost_piva_2 = 138
stoimost_piva_3 = 86
stoimost_piva_4 = 94
stoimost_piva_5 = 67

kolichestvo_piva_1 = 2
kolichestvo_piva_2 = 3
kolichestvo_piva_3 = 1
kolichestvo_piva_4 = 0
kolichestvo_piva_5 = 4

tvoya_kupura = 1000

summa = ((stoimost_piva_1*kolichestvo_piva_1) + (stoimost_piva_2*kolichestvo_piva_2) +
         (stoimost_piva_3*kolichestvo_piva_3) +(stoimost_piva_4*kolichestvo_piva_4) +
         (stoimost_piva_5*kolichestvo_piva_5))

tvoya_sdacha = 1000-summa

print('Всё пиво будет стоить', summa)
print('Тебе должны сдачу в размере', tvoya_sdacha, 'рублей')