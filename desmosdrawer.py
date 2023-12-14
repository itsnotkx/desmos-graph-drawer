import cv2 as cv
import subprocess
import xml.etree.ElementTree as ET
low_threshold=50
max_threshold=100

def cannyfunction(low_threshold):
    edges=cv.Canny(greyscale_image,low_threshold,max_threshold)
    inverse_edges=cv.bitwise_not(edges)
    cv.imshow("Image preview",inverse_edges)

def greyscaleimage():
    image_name=input("Enter file directory for desired image here:")
    greyscale_image=cv.imread(image_name,cv.IMREAD_GRAYSCALE)
    if image_name:
        return greyscale_image,image_name
    else:
        return "Image not found: Please try again"

def save_image():
    edges=cv.Canny(greyscale_image,low_threshold,max_threshold)
    inverse_edges=cv.bitwise_not(edges)
    bitmap_name=image_name.strip(".jpg")+"bitmap.bmp"
    cv.imwrite(bitmap_name,inverse_edges)
    print("Image saved under " + bitmap_name)
    return bitmap_name
    
burger_meat=""""""
end_parse=False
x_anchor_coord=0
y_anchor_coord=0
burger_top_bun="""<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <script src="https://www.desmos.com/api/v1.8/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
        </head>
    <body>
        <div id="calculator" style="width: 1920px; height: 1080px;"></div>
        <script>
                var elt = document.getElementById('calculator');
                var calculator = Desmos.GraphingCalculator(elt);\n"""
burger_bottom_bun="""    </script>
    </body>
    </html>"""


def potraceimage(bitmap_name):
    try:
        print("Converting bitmap into svg file format...")
        svg_file_name = bitmap_name.replace(".bmp", ".svg")
        subprocess.run(["potrace", bitmap_name, "-b", "svg","-o", svg_file_name])
    except subprocess.CalledProcessError as e:
        print ("An error has occured, image unable to be converted, reason: ",e)
    return svg_file_name

def nextcommand(general_list):
    path_command_list=[]
    path_command_list.append(len(general_list)+1)
    for index,item in enumerate(general_list):
        if "m" in item:
            path_command_list.append(index)
        elif "l" in item:
            path_command_list.append(index)
        elif "c" in item:
            path_command_list.append(index)
        elif "M" in item:
            path_command_list.append(index)
        else:
            pass
    path_command_list.sort()
    return path_command_list

def anchor_parsing(i,general_list,anchor_count):
    x_anchor_coord=general_list[i].removeprefix("M")
    y_anchor_coord=general_list[i+1]
    anchor_count+=1
    return x_anchor_coord,y_anchor_coord,anchor_count

def moveto(general_list,x_anchor_coord,y_anchor_coord,i):
    x_anchor_coord=int(x_anchor_coord)+int(general_list[i].removeprefix("m"))
    y_anchor_coord=int(y_anchor_coord)+int(general_list[i+1])
    return x_anchor_coord,y_anchor_coord,i

def line_parsing(general_list,next_command,x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,i,command_count,end_parse):
    x_list=[]
    y_list=[]
    current_count=i
    stop_count=next_command[command_count+1]
    old_x_anchor=x_anchor_coord
    old_y_anchor=y_anchor_coord

    for coord in general_list[current_count:stop_count+1]:
        print (current_count)
        print(stop_count)
        if "m" in general_list[current_count]:
            linear_counter+=1
            print (x_list,y_list)
            burger_meat+="            calculator.setExpression({"+"type:'table',columns:[{"+"latex:'x_{t"+str(linear_counter)+"}',values:"+str(x_list)+"},{latex:'y_{t"+str(linear_counter)+"}',values:"+str(y_list)+",lines:true"+",pointOpacity:0"+"}]});\n"
            return x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse
        if "M" in general_list[current_count]:
            linear_counter+=1
            print (x_list,y_list)
            burger_meat+="            calculator.setExpression({"+"type:'table',columns:[{"+"latex:'x_{t"+str(linear_counter)+"}',values:"+str(x_list)+"},{latex:'y_{t"+str(linear_counter)+"}',values:"+str(y_list)+",lines:true"+",pointOpacity:0"+"}]});\n"
            return x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse
        if "c" in general_list[current_count]:
            linear_counter+=1
            print (x_list,y_list)
            burger_meat+="            calculator.setExpression({"+"type:'table',columns:[{"+"latex:'x_{t"+str(linear_counter)+"}',values:"+str(x_list)+"},{latex:'y_{t"+str(linear_counter)+"}',values:"+str(y_list)+",lines:true"+",pointOpacity:0"+"}]});\n"
            return x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse
        if "z" in general_list[current_count]:
            x_list.append(old_x_anchor)
            y_list.append(old_y_anchor)
            x_anchor_coord=old_x_anchor
            y_anchor_coord=old_y_anchor
            burger_meat+="            calculator.setExpression({"+"type:'table',columns:[{"+"latex:'x_{t"+str(linear_counter)+"}',values:"+str(x_list)+"},{latex:'y_{t"+str(linear_counter)+"}',values:"+str(y_list)+",lines:true"+",pointOpacity:0"+"}]});\n"
            linear_counter+=1
            return x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse
        if "END" in general_list[current_count]:
            print("STOP!")
            end_parse=True
            return x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse
        if current_count%2==0:
            x_anchor_coord=int(x_anchor_coord)+int(general_list[current_count].removeprefix("l"))
            x_list.append(x_anchor_coord)
            current_count+=1
        elif current_count%2!=0:
            y_anchor_coord=int(y_anchor_coord)+int(general_list[current_count])
            y_list.append(y_anchor_coord)
            current_count+=1

def curve_parsing(general_list,next_command,x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,i,command_count,end_parse):
    x_c_list=[]
    y_c_list=[]
    old_x_anchor=x_anchor_coord
    old_y_anchor=y_anchor_coord
    current_count=i
    stop_count=next_command[command_count+1]
    print(len(general_list))
    for coord in general_list[current_count:stop_count]:
        if "m" in general_list[current_count]:
            return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse
        elif "M" in general_list[current_count]:
            return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse
        elif "l" in general_list[current_count]:
            return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse
        if "END" in general_list[stop_count-2]:
            end_parse=True
            print ("STOP!")
            return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse        

        point_a_x=int(x_anchor_coord)
        point_a_y=int(y_anchor_coord)
        burger_meat+="            calculator.setExpression({ id: "+'"pa'+str(cubic_counter)+'", latex: "A_{'+str(cubic_counter)+"}="+f'({point_a_x},{point_a_y})"'+",hidden:true"+"});"+"\n"

        point_b_x=int(x_anchor_coord)+int(general_list[current_count].removeprefix("c"))
        current_count+=1
        point_b_y=int(y_anchor_coord)+int(general_list[current_count])
        current_count+=1
        burger_meat+="            calculator.setExpression({ id: "+'"pb'+str(cubic_counter)+'", latex: "B_{'+str(cubic_counter)+"}="+f'({point_b_x},{point_b_y})"'+",hidden:true"+"});"+"\n"

        point_c_x=int(x_anchor_coord)+int(general_list[current_count])
        current_count+=1
        point_c_y=int(y_anchor_coord)+int(general_list[current_count])
        current_count+=1
        burger_meat+="            calculator.setExpression({ id: "+'"pc'+str(cubic_counter)+'", latex: "C_{'+str(cubic_counter)+"}="+f'({point_c_x},{point_c_y})"'+",hidden:true"+"});"+"\n"

        point_d_x=int(x_anchor_coord)+int(general_list[current_count])
        current_count+=1
        point_d_y=int(y_anchor_coord)+int(general_list[current_count].removesuffix("z"))
        current_count+=1
        burger_meat+="            calculator.setExpression({ id: "+'"pd'+str(cubic_counter)+'", latex: "D_{'+str(cubic_counter)+"}="+f'({point_d_x},{point_d_y})"'+",hidden:true"+"});"+"\n"
        burger_meat+="            calculator.setExpression({ id: "+'"c'+str(cubic_counter)+'", latex: "X_{'+str(cubic_counter)+"}=(1-t)^3(A_{"+str(cubic_counter)+"})+3(1-t)^2t(B_{"+str(cubic_counter)+"})+3(1-t)t^2(C_{"+str(cubic_counter)+"})+t^3(D_{"+str(cubic_counter)+'})"});'+"\n"
        if "z" in general_list[current_count+1]:
            print ("z spotted")
            x_c_list.append(point_d_x)
            y_c_list.append(point_d_y)
            x_c_list.append(int(old_x_anchor))
            y_c_list.append(int(old_y_anchor))
            burger_meat+="            calculator.setExpression({"+"type:'table',columns:[{"+"latex:'x_{t"+str(int(cubic_counter)+1)+"}',values:"+str(x_c_list)+"},{latex:'y_{t"+str(int (cubic_counter))+"}',values:"+str(y_c_list)+",lines:true"+",pointOpacity:0"+"}]});\n"
            cubic_counter+=1
            x_anchor_coord=old_x_anchor
            y_anchor_coord=old_y_anchor
            return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse
        else:
            x_anchor_coord=point_d_x
            y_anchor_coord=point_d_y
            cubic_counter+=1
            if "END" in general_list[current_count]:
                end_parse=True
                print("STOP!")
                return x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse

def looper(x_anchor_coord,y_anchor_coord,burger_meat,end_parse):
    anchor_count=0
    i=0
    linear_counter=0
    cubic_counter=0
    command_count=0
    end_parse=False
    general_list=[]
    for path in path_elements:
        path_data = path.get("d")
        for item in path_data.split():
            general_list.append(item)
    general_list.append("END")
    next_command=nextcommand(general_list)
    
    for coord in general_list:
        if end_parse==True:
            print('html will be stored in file named "html folder\n"')
            print('To change file name, edit the desired_file variable.')
            desired_file=""

            desmos_html_file=open(desired_file,"w")
            desmos_html_file.write(burger_top_bun)
            desmos_html_file.write(burger_meat)
            desmos_html_file.write(burger_bottom_bun)
            desmos_html_file.close()
            return desired_file
        elif "M" in coord:
            x_anchor_coord,y_anchor_coord,anchor_count,=anchor_parsing(i,general_list,anchor_count)
            command_count+=1
            i=next_command[command_count]
            if i==len(general_list):
                break
        elif "l" in coord:
            x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,end_parse=line_parsing(general_list,next_command,x_anchor_coord,y_anchor_coord,linear_counter,burger_meat,i,command_count,end_parse)
            command_count += 1
            i = next_command[command_count]
            if i==len(general_list):
                break
        elif "c" in coord:
            x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,end_parse=curve_parsing(general_list,next_command,x_anchor_coord,y_anchor_coord,cubic_counter,burger_meat,i,command_count,end_parse)
            command_count+=1
            i=next_command[command_count]
            if i==len(general_list):
                break
        elif "m" in coord:
            x_anchor_coord,y_anchor_coord,i=moveto(general_list,x_anchor_coord,y_anchor_coord,i)
            command_count+=1
            i=next_command[command_count]
            if i==len(general_list):
                break

if __name__=="__main__":
    greyscale_image,image_name=greyscaleimage()
    cv.namedWindow("Image preview",cv.WINDOW_NORMAL)
    cv.resizeWindow("Image preview",1920,1080)
    cv.createTrackbar("Canny-meter","Image preview", low_threshold, 100, cannyfunction)
    key=cv.waitKey(0)
    if key == 13:
        print("Generating image bitmap...")
        saved_bitmap_name=save_image()
        svg_file_name=potraceimage(saved_bitmap_name)
    elif key != 255:
        print("Process cancelled")
        cv.destroyAllWindows

    tree=ET.parse(svg_file_name)
    root=tree.getroot()
    svg_namespace = "{http://www.w3.org/2000/svg}"
    path_elements = root.findall(".//{}path".format(svg_namespace))
    desired_file=looper(x_anchor_coord,y_anchor_coord,burger_meat,end_parse)
    if end_parse==True and desired_file is not None:
        print("Your html file is ready to view at "+desired_file+", file may take some time to load.")