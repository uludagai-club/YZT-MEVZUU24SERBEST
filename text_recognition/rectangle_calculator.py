import copy
import sys
import os
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.pdf_to_image import Pdf_to_image

class RectangleCalculator:
    def __init__(self,sections,max_width,max_height) -> None:
        self.sections=sections
        self.max_width=max_width
        self.max_height=max_height
    
    def remain_rectangles(self,first_rectangle, second_rectangle):
        x1_first, y1_first, x2_first, y2_first = first_rectangle
        x1_second, y1_second, x2_second, y2_second = second_rectangle

        remaining_rectangles = []
        for x1, y1, x2, y2 in [(x1_first, y1_first, x2_first, y1_second),
                            (x1_first, y1_second, x1_second, y2_second),
                            (x1_second, y1_first, x2_second, y1_second),
                            (x2_second, y1_second, x2_first, y2_second)]:
            if x1 < x2 and y1 < y2:
                remaining_rectangles.append((x1, y1, x2, y2))

        return remaining_rectangles


    def unified_rectangle(self,inner_rectangles):
        x1, y1, x2, y2 = inner_rectangles[0]
        
        
        for inner_rectangle in inner_rectangles[1:]:
            x1 = min(x1, inner_rectangle[0])
            y1 = min(y1, inner_rectangle[1])
            x2 = max(x2, inner_rectangle[2])
            y2 = max(y2, inner_rectangle[3])
        
        return (x1, y1, x2, y2)
    
    def check_rectangle(self,rectangle):
        x1,y1,x2,y2=rectangle
        temp=0
        if x1>x2:
            temp=x2
            x1=x2
            x2=temp
        
        temp=0
        if y1>y2:
            temp=y2
            y1=y2
            y2=temp
        
        return (x1,y1,x2,y2)
    
    def print_rectangle(self,ax, rectangle, color):
        x1, y1, x2, y2 = rectangle
        ax.add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor=color, facecolor='none'))

    def rectangle_painter(self,x1=0,y1=0,inner_rectangle=[0,0,0,0],rectangle_1=[0,0,0,0],rectangle_2=[0,0,0,0],rectangle_3=[0,0,0,0]):
        fig, ax = plt.subplots()
        self.print_rectangle(ax, rectangle_1, 'red')
        self.print_rectangle(ax, rectangle_2, 'blue')
        self.print_rectangle(ax, rectangle_3, 'green')
        
        ax.set_xlim(0, self.max_width+100)
        ax.set_ylim(self.max_height+100)
        plt.show()
        print("aaa")
    
    def find_rectangles(self):
        self.rectangels=copy.deepcopy(self.sections)
        
        for section_index in self.sections:
            x1,y1,x2,y2=self.sections[section_index]["rectangle"]
            in_rectangles=[]
            
            for other_section_index in  self.sections:
                if section_index==other_section_index:
                    continue
                other_x1,other_y1,other_x2,other_y2= self.sections[other_section_index]["rectangle"]
                
                if ((other_x1>x2 and ((y1 <= other_y1  and other_y1 <= y2) or (y1 <= other_y2 and other_y2 <= y2))) or 
                    (other_y1>y2 and ((x1 <= other_x1  and other_x1 <= x2) or (x1 <= other_x2 and other_x2 <= x2)))
                    ):
                
                    in_rectangles.append((other_x1, other_y1, self.max_width, self.max_height))
            
            
            if len(in_rectangles)>0:
                inner_rectangle=self.unified_rectangle(in_rectangles)
            else:
                inner_rectangle=(self.max_width,self.max_height,self.max_width,self.max_height)
            
            remain_rectangles=self.remain_rectangles((x1,y1,self.max_width,self.max_height),inner_rectangle)
                
            try:
                if x2>remain_rectangles[0][2]:
                    rectangle_1=(x2,y1,x2,y2)
                else:
                    rectangle_1=(x2,y1,remain_rectangles[0][2],y2)
                    
                rectangle_2=(x1,y2,remain_rectangles[0][2],remain_rectangles[0][3])
            except:
                rectangle_1=(0,0,0,0)
                rectangle_2=(0,0,0,0)
            try:
                rectangle_3=(x1,rectangle_2[3],remain_rectangles[1][2],remain_rectangles[1][3])
            except:
                rectangle_3=(0,0,0,0)
            
                            
            self.rectangels[section_index]["rectangle_1"]=self.check_rectangle(rectangle_1)
            self.rectangels[section_index]["rectangle_2"]=self.check_rectangle(rectangle_2)
            self.rectangels[section_index]["rectangle_3"]=self.check_rectangle(rectangle_3)
                
        self.sections=copy.deepcopy(self.rectangels)
        


# if __name__=="__main__":

#     sections = {12: {"rectangle":(40, 40, 240, 240)},24: {"rectangle":(280, 140, 400, 320)},36: {"rectangle":(30, 330, 460, 550)}}

#     rectangle_calculator=RectangleCalculator(sections, 793,1122)
#     rectangle_calculator.find_rectangles()
    
#     pdf_to_image=Pdf_to_image("docs/resumes/blank.pdf")
#     pages=pdf_to_image.get_pages()