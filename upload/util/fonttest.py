import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


font_name = fm.FontProperties(fname="/home/ubuntu/study/malgun.ttf").get_name()
print(font_name)

