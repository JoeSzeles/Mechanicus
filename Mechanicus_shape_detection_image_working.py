import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk, messagebox, Scrollbar
from tkinter.filedialog import askopenfilename, asksaveasfilename
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import END
import inspect
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.spatial import KDTree
import dxfgrabber
from math import hypot
import xml.etree.ElementTree as ET
from simplepath import parsePath, formatPath
import svgwrite
import math
#import cairosvg
from svgtrace import trace
from pathlib import Path
var1 = None
# Create PhotoImage object as a global variable
photo = None


    
def svg_to_png():
    svg_path=askopenfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
    png_path=asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")]) 
    """
    Converts an SVG file to PNG format and saves it to the specified path.

    Args:
    svg_path (str): Path to the SVG file.
    png_path (str): Path to save the PNG file.
    """
    #cairosvg.svg2png(url=svg_path, write_to=png_path)

def Imagevector():
    window = Tk()
    window.title("MECHANICUS_V.0.1 Beta. (c)Reservoir Frogs 2022")
    window.configure(bg="#263d42", borderwidth=0)
    window.geometry("600x800+1200+160")

    #Checkboxes
    # Create the checkbox variable
    def update_progress():
        for i in range(101):
            progress_bar["value"] = i
            window.update_idletasks()
            
    def load_image():
        filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        out=Image.open(filename)
        out.save(".\\temp2.png")
        out_photo = ImageTk.PhotoImage(out)
        # Create the canvas image item and store its I
        # Create Tkinter PhotoImage object with new im
         
    
        # Update the PhotoImage object held by the lab
        label.configure(image=out_photo)
        label.image = out_photo  # Store a reference t
    
        # Update the scroll region of the canvas to in
        canvas.config(scrollregion=canvas.bbox("all"))
        
    def convert_image_to_svg(input_image_path, bw=False):
        # Get the absolute path of the parent directory of the current file
        THISDIR = str(Path(__file__).resolve().parent)

        # Define the file path for the input image without extension
        input_image_file = Path(input_image_path).resolve()
        input_image_basename = input_image_file.stem
        input_image_dirname = input_image_file.parent
        output_filename = f"{input_image_basename}.svg"
        sensitivity1 = int(edge_complexity_input.get())
        threshold = int(lower_treshold_input.get())
        tolerance = int(contour_range_input.get())
        optimize = int(edge_complexity_input.get())
        scale = float(incrase_resolution_input.get())
        blur =  float(alpha_input1.get())
        if bw:
            output_filename = f"{input_image_basename}-bw.svg"

        output_file_path = input_image_dirname / output_filename

        # Convert the input image into an SVG file and save it
        Path(output_file_path).write_text(trace(str(input_image_file), bw))
        update_progress() 
        
    def svg_trace():
        # Open a file dialog to choose an image file
        input_image_path = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])

        if input_image_path:
            # Convert the image to SVG
            convert_image_to_svg(input_image_path)

            # Show a message box indicating that the conversion is complete
            tk.messagebox.showinfo("Conversion Complete", f"{input_image_path} has been converted to SVG!") 
            update_progress() 
            
            
    def rotate_svg(svg_path):
        # Load SVG file
        svg = svgwrite.Drawing(svg_path)

        # Get SVG width and height
        width = int(svg.attribs['width'].rstrip('px').rstrip('%'))
        height = int(svg.attribs['height'].rstrip('px').rstrip('%'))

        # Create a new SVG object with rotated dimensions
        new_width = math.ceil(abs(width * math.cos(math.radians(45))) + abs(height * math.sin(math.radians(45))))
        new_height = math.ceil(abs(height * math.cos(math.radians(45))) + abs(width * math.sin(math.radians(45))))
        new_svg = svgwrite.Drawing(size=(new_width, new_height))

        # Rotate original SVG and add to new SVG
        new_svg.add(svg.rotate(-45, (width/2, height/2)))

        # Save new SVG file
        save_svg_path = svg_path[:-4] + '_rotated.svg'
        new_svg.saveas(save_svg_path)

        # Close SVG files
        svg.close()
        new_svg.close()

        print("SVG file saved successfully")
        
    def path_Length(path):
        """Compute the length of a path"""
        length = 0
        for i in range(len(path)-1):
            p1 = path[i]
            p2 = path[i+1]
            length += np.linalg.norm(p2-p1)
        return length


    def simplify_path(path, tolerance):
        """Simplify a path by removing points that are farther than the tolerance from the straight line connecting their neighbors."""
        path = np.array(path, dtype=float)
        if len(path) < 3:
            return path.tolist()

        # Find the point with the maximum distance from the line connecting the endpoints
        dists = np.linalg.norm(np.cross(path[1:] - path[0], path[:-1] - path[0]), axis=1) / np.linalg.norm(path[1:] - path[:-1], axis=1)
        i = np.argmax(dists)
        if dists[i] > tolerance:
            # Recursively simplify the two sub-paths
            subpath1 = simplify_path(path[:i+1], tolerance)
            subpath2 = simplify_path(path[i:], tolerance)
            # Remove the duplicate point where the subpaths meet
            if subpath1[-1] == subpath2[0]:
                subpath1.pop()
            # Combine the subpaths and remove any duplicates
            combined_subpath = subpath1[:-1] + subpath2
            combined_subpath = list(set(tuple(point) for point in combined_subpath))
            combined_subpath = [list(point) for point in combined_subpath]
            # Add back the endpoint of the original path
            combined_subpath.append(path[-1])
            return combined_subpath
        else:
            return [path[0], path[-1]]


    def cleanup_svg():
        """Opens an SVG file and removes any paths with less than 2 points, a length under the specified minimum length, or stray points.
        Saves the resulting SVG file to the specified output file path."""
        svg_file_path = askopenfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
        output_file_path =asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
        min_path_length = 10
        max_point_distance = 1

        # Parse the SVG file
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # Simplify each path and remove any with less than 2 points or a length under the specified minimum length
        for path in root.iter('path'):
            path_str = path.get('d')
            path_list = parsePath(path_str)
            path_list = [simplify_path(subpath, max_point_distance) for subpath in path_list]
            path_list = [subpath for subpath in path_list if len(subpath) >= 2]
            path_str = formatPath(path_list)
            path_length = path_Length(path_str)
            if path_length < min_path_length:
                root.remove(path)
            else:
                path.set('d', path_str)

        # Save the modified SVG file
        tree.write(output_file_path)
     
    
    def optimized_imagevector():

        # Get input values from the input boxes
        incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_treshold = int(lower_treshold_input.get()) #lower treshold
        upper_treshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        outline = int(outline_input.get()) #outline thickness
        vertices = int(vertices_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        optimize_tres = int(vertices_input.get()) #outline thickness
        filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
        # Open a dialog box to select the input file
        Tk().withdraw()  # to hide the main window
        # Load the input image
        img = cv2.imread(filename, 1)
        img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
        thr = np.zeros_like(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray)
        # Increase the contrast of the grayscale image
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        cv2.blur(img, (1, 1), img)
        thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)
        contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        center = [None] * len(contours)
        radius = [None] * len(contours)
        hull = [None] * len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, vertices, True)
            if len(contours_poly[i]) > edge_complexity:
                cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
            else:
                cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))
        # Show the original image with contours overlaid
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.show()
        # Create an image with just the contours as SVG File
        thr = cv2.cvtColor(thr, cv2.COLOR_grayRGB)
        for i, c in enumerate(contours_poly):
            if len(c) > optimize_tres:
                cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
            else:
                cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
        img_thr = Image.fromarray(cv2.cvtColor(thr, cv2.COLOR_BGR2RGB))
        with open(save_svg_path, 'w') as f:
            f.write('<svg viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg">'.format(img.shape[1], img.shape[0]))
            for i, contour in enumerate(contours_poly):
                if len(contour) >= optimize_tres:
                    # simplify the path with cv2.approxPolyDP
                    contour = cv2.approxPolyDP(contour, vertices, True)
                    if len(contour) >= 3:
                        path_string = 'M '
                        start_point = contour[0].squeeze()
                        path_string += '{} {} '.format(start_point[0], start_point[1])
                        if len(contour) == 3:
                            end_point = contour[-1].squeeze()
                            path_string += 'Q {} {} {} {} '.format(contour[1].squeeze()[0], contour[1].squeeze()[1], end_point[0], end_point[1])
                        else:
                            path_string += 'C '
                            for i in range(1, len(contour)-contour_range, contour_range):
                                c1 = contour[i].squeeze()
                                c2 = contour[i+1].squeeze()
                                end_point = contour[i+2].squeeze()
                                path_string += '{} {} {} {} {} {} '.format(c1[0], c1[1], c2[0], c2[1], end_point[0], end_point[1])
                        path_string += 'Z '
                        f.write('<path d="{}" stroke="black" stroke-width="2" fill="none" />'.format(path_string))
            f.write('</svg>')
    def run_imagevector():

            # Get input values from the input boxes
            incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
            lower_treshold = int(lower_treshold_input.get()) #lower treshold
            upper_treshold = int(upper_treshold_input.get())
            edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
            contour_range = int(contour_range_input.get())
            outline = int(outline_input.get()) #outline thickness
            vertices = int(vertices_input.get()) #outline thickness
            alpha =  float(alpha_input1.get()) # contrast multiplier
            beta = float(beta_input.get())  # shift factor
            filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
            save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
            # Open a dialog box to select the input file
            Tk().withdraw()  # to hide the main window


            # Load the input image
            img = cv2.imread(filename, 1)
            img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
            thr = np.zeros_like(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.convertScaleAbs(gray)
            # Increase the contrast of the grayscale image

            gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
            cv2.blur(img, (1, 1), img)
            thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)

            contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_poly = [None] * len(contours)
            boundRect = [None] * len(contours)
            center = [None] * len(contours)
            radius = [None] * len(contours)
            hull = [None] * len(contours)

            for i, c in enumerate(contours):
                contours_poly[i] = cv2.approxPolyDP(c, vertices, True)

                if len(contours_poly[i]) > edge_complexity:
                    cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
                else:
                    cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))

            # Show the original image with contours overlaid
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img.show()


            # Create an image with just the contours as SVG File
            thr = cv2.cvtColor(thr, cv2.COLOR_grayRGB)
            for i, c in enumerate(contours_poly):
                if len(c) > edge_complexity:
                    cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
                else:
                    cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
            img_thr = Image.fromarray(cv2.cvtColor(thr, cv2.COLOR_BGR2RGB))

            with open(save_svg_path, 'w') as f:
                f.write('<svg viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg">'.format(img.shape[1], img.shape[0]))
                for i, contour in enumerate(contours_poly):
                    if len(contour) >= 2:  # add check to ensure that contour has at least two points
                        path_string = 'M '
                        for point in contour.squeeze():
                            path_string += '{},{} '.format(point[0], point[1])
                        path_string += 'Z '
                        if len(contour) > 15:
                            f.write(f'<path d="{path_string}" stroke="green" stroke-width="2" fill="none" />')
                        else:
                            f.write(f'<path d="{path_string}" stroke="red" stroke-width="2" fill="none" />')
                f.write('</svg>')

    def png_save():

            # Get input values from the input boxes
            incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
            lower_treshold = int(lower_treshold_input.get()) #lower treshold
            upper_treshold = int(upper_treshold_input.get())
            edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
            contour_range = int(contour_range_input.get())
            outline = int(outline_input.get()) #outline thickness
            vertices = int(vertices_input.get()) #outline thickness
            alpha =  float(alpha_input1.get()) # contrast multiplier
            beta = float(beta_input.get())  # shift factor
            
            filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
            save_png_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")]) 
            # Open a dialog box to select the input file
            Tk().withdraw()  # to hide the main window


            # Load the input image
            img = cv2.imread(filename, 1)
            img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
            thr = np.zeros_like(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.convertScaleAbs(gray)
            # Increase the contrast of the grayscale image

            gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
            cv2.blur(img, (1, 1), img)
            thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)

            contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_poly = [None] * len(contours)
            boundRect = [None] * len(contours)
            center = [None] * len(contours)
            radius = [None] * len(contours)
            hull = [None] * len(contours)

            for i, c in enumerate(contours):
                contours_poly[i] = cv2.approxPolyDP(c, vertices, True)

                if len(contours_poly[i]) > edge_complexity:
                    cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
                else:
                    cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))

            # Show the original image with contours overlaid
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img.show()

            # Create an image with just the contours
            thr = cv2.cvtColor(thr, cv2.COLOR_grayRGB)
            for i, c in enumerate(contours_poly):
                if len(c) > 15:
                    cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
                else:
                    cv2.drawContours(thr, contours_poly, i, (255, 255, 255), outline, 8, hierarchy, 0, (0, 0))
            img_thr = Image.fromarray(cv2.cvtColor(thr, cv2.COLOR_BGR2RGB))
            img_thr.show()
            cv2.imwrite(save_png_path, cv2.cvtColor(thr, cv2.COLOR_BGR2RGB))
            
            
    def run_linevector():

        # Get input values from the input boxes
        incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_treshold = int(lower_treshold_input.get()) #lower treshold
        upper_treshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        vertices = int(vertices_input.get()) #outline thickness
        outline = int(outline_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        minLineL= int(minLineL_input.get()) #minimun line Lenght
        LineGap = int(LineGap_input.get()) #maximum line gap
        # Open a dialog box to select the input file
        Tk().withdraw()  # to hide the main window
        filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")]) 
        # Open a dialog box to select the input file
        Tk().withdraw()  # to hide the main window
        # Load the input image
        img = cv2.imread(filename, 1)
        img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
        thr = np.zeros_like(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray)
        # Increase the contrast of the grayscale image
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        cv2.blur(img, (1, 1), img)
        thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)
        contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        center = [None] * len(contours)
        radius = [None] * len(contours)
        hull = [None] * len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, vertices, True)
            if len(contours_poly[i]) > edge_complexity:
                cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
            else:
                cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))
        # Show the original image with contours overlaid
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.show()
        # Create an image with just the contours
        thr = cv2.cvtColor(thr, cv2.COLOR_grayRGB)


        # Convert the image to grayscale
        gray_img = cv2.cvtColor(thr, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to the grayscale image
        _, thresh_img = cv2.threshold(gray_img, lower_treshold, 255, cv2.THRESH_BINARY)
        
        # Apply the Hough transform to detect lines
        lines = cv2.HoughLinesP(thresh_img, 1, np.pi/180, threshold=lower_treshold, minLineLength=minLineL, maxLineGap=LineGap)


        # Draw the detected lines on the original image
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=outline)

        # Show the original image with detected lines overlaid
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.show()

        # Create an image with just the detected lines as SVG file
        with open(save_svg_path, 'w') as f:
            f.write('<svg viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg">'.format(img.shape[1], img.shape[0]))
            for line in lines:
                x1, y1, x2, y2 = line[0]
                f.write(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="green" stroke-width="2" />')
            f.write('</svg>')





    def create_particles(contours, num_particles, radius_range, center_range):
        particles = []
        for c in contours:
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            radius = random.uniform(radius_range[0], radius_range[1])
            for i in range(num_particles):
                x = int(random.gauss(center_x, center_range[0]))
                y = int(random.gauss(center_y, center_range[1]))
                particle = [x, y]
                particles.append(particle)
        return particles


    def run_particle():
    
        # Get input values from the input boxes
        increase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_threshold = int(lower_treshold_input.get()) #lower treshold
        upper_threshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        outline = int(outline_input.get()) #outline thickness
        vertices = int(vertices_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        particle_density = int(particle_density_input.get())  # particle density
        particle_density_edges = int(particle_density_edges_input.get())  # particle density edges
        # Open a dialog box to select the input file
        Tk().withdraw()  # to hide the main window
        filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    
        # Load the input image
        img = cv2.imread(filename, 1)
        img = cv2.resize(img, None, fx=increase_resolution, fy=increase_resolution, interpolation=cv2.INTER_LINEAR)
    
        # Convert the image to grayscale and increase its contrast
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
        # Detect edges using the Canny edge detection algorithm
        edges = cv2.Canny(gray, lower_threshold, upper_threshold, None, 3, False)
    
        # Find contours of the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        # Create particles inside each detected shape
        particles = create_particles(contours, num_particles=particle_density, radius_range=(1, 5), center_range=(20, 20))
    
        # Add particles along the contour edges
        for c in contours:
            
            particles += create_particles([c], num_particles=particle_density_edges, radius_range=(0, 1), center_range=(0, 1))
    
        # Triangulate the particles
        tri = Delaunay(particles)

        # Draw the Delaunay triangulation on the image
        for i in range(len(tri.simplices)):
            vertices = tri.points[tri.simplices[i]]
            #cv2.line(img, (int(vertices[0][0]), int(vertices[0][1])), (int(vertices[1][0]), int(vertices[1][1])), (0, 255, 0), 1)
            #cv2.line(img, (int(vertices[1][0]), int(vertices[1][1])), (int(vertices[2][0]), int(vertices[2][1])), (255, 0, 0), 1)
            cv2.line(img, (int(vertices[2][0]), int(vertices[2][1])), (int(vertices[0][0]), int(vertices[0][1])), (0, 255, 0), 1)
    
        # Show the image with Delaunay triangulation
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
        # Create a blank image of the same size as img
        blank_image = np.zeros_like(img)

        # Draw the Delaunay triangles on the blank image
        for i in range(len(tri.simplices)):
            vertices = tri.points[tri.simplices[i]]
            cv2.line(blank_image, (int(vertices[0][0]), int(vertices[0][1])), (int(vertices[1][0]), int(vertices[1][1])), (255, 0, 0), 1)
            cv2.line(blank_image, (int(vertices[1][0]), int(vertices[1][1])), (int(vertices[2][0]), int(vertices[2][1])), (0, 255, 0), 1)
            cv2.line(blank_image, (int(vertices[2][0]), int(vertices[2][1])), (int(vertices[0][0]), int(vertices[0][1])), (0, 0, 255), 1)

        # Show the image with Delaunay triangulation
        plt.imshow(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
        plt.show()
        # Overlay contours on the original image
        contours_img = cv2.drawContours(blank_image, contours, -1, (255, 255, 255), outline)

        # Show the image with contours overlayed
        plt.imshow(cv2.cvtColor(contours_img, cv2.COLOR_BGR2RGB))
        plt.show()
                # Draw particles
        image_width, image_height = contours_img.shape[:2]
        radius=1
        image = Image.new('RGB', (image_width, image_height), color='black')
        draw = ImageDraw.Draw(image)
        for particle in particles:
            x, y = particle
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='yellow')
    
        # Display or save the image
        image.show()
        # OR
        image.save('output.png')
        
        
        from scipy.spatial import KDTree

        # Convert particles to a NumPy array
        particles = np.array(particles)

        # Find the nearest neighbors of each particle
        kdtree = KDTree(particles)
        distances, indices = kdtree.query(particles, k=3)
        blank_image = np.zeros_like(img)
        # Draw the nearest neighbor connections on the image
        for i in range(len(particles)):
            for j in indices[i][1:]:
                p1 = particles[i].astype(int)
                p2 = particles[j].astype(int)
                cv2.line(blank_image, (p1[0], p1[1]), (p2[0], p2[1]), (255, 255, 0), 1)

        # Show the image with nearest neighbor connections
        plt.imshow(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
        plt.show()
      

    
    def Image_to_Particle():
        # Get input values from the input boxes
        
        increase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_threshold = int(lower_treshold_input.get()) #lower treshold
        upper_threshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        outline = int(outline_input.get()) #outline thickness
        vertices = int(vertices_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        particle_density = int(particle_density_input.get())  # particle density
        particle_density_edges = int(particle_density_edges_input.get())  # particle density edges
        tolerance = 1  # adjust the tolerance value as needed
        # Load the image
        #filename = askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        filename = "temp2.png"
        img = cv2.imread(filename)
        img = cv2.resize(img, None, fx=increase_resolution, fy=increase_resolution, interpolation=cv2.INTER_LINEAR)
        particle_density = int(particle_density_input.get())  # particle density
        particle_distance=int(particle_distance_input.get())  #Partice distance
        particle_connections=int(particle_connections_input.get())  #Partice distance
        # Add particles on black pixels
        particles = []
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                if img[y, x, 0] == 0 and img[y, x, 1] == 0 and img[y, x, 2] == 0:
                    particles.append((x, y))

        # Remove every 3rd particle
        particles = particles[::particle_density ]

        # Create an image with the particles drawn on it
        img_with_particles = np.zeros_like(img)
        for p in particles:
            cv2.circle(img_with_particles, p, 1, (255, 255, 255), -1)

        # Display the result
        plt.imshow(cv2.cvtColor(img_with_particles, cv2.COLOR_BGR2RGB))
        plt.show()

        # Convert particles to a NumPy array
        particles = np.array(particles)

        # Find the nearest neighbors of each particle
        kdtree = KDTree(particles)
        distances, indices = kdtree.query(particles, k=particle_connections)
        blank_image = np.zeros_like(img_with_particles)

        # Draw the nearest neighbor connections on the image
        if (distances < particle_distance).all():
            for i in range(len(particles)):
                for j in indices[i][1:]:
                    p1 = particles[i].astype(int)
                    p2 = particles[j].astype(int)
                    cv2.line(blank_image, (p1[0], p1[1]), (p2[0], p2[1]), (255, 255, 255), 1)

        # Show the image with nearest neighbor connections
        plt.imshow(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
        plt.show()
        
        save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")])
        # Save the image with nearest neighbor connections as SVG file
        with open(save_svg_path, "w") as f:
            f.write(f'<svg viewBox="0 0 {blank_image.shape[1]} {blank_image.shape[0]}" xmlns="http://www.w3.org/2000/svg">\n')
            prev_coord = None
            for i in range(len(particles)):
                for j in indices[i][1:]:
                    p1 = particles[i]
                    p2 = particles[j]
                    coord1 = (int(p1[0]), int(p1[1]))
                    coord2 = (int(p2[0]), int(p2[1]))
                    if prev_coord is None or np.linalg.norm(np.array(prev_coord) - np.array(coord1)) >= tolerance:
                        f.write(f'<path stroke="white" stroke-width="1" fill="none" d="M{coord1[0]},{coord1[1]} ')
                        prev_coord = coord1
                    f.write(f'L{coord2[0]},{coord2[1]} ')
                f.write('" />\n')
            f.write('</svg>')
        print("SVG file saved successfully")





    def Image_to_svg():
        # Ask for the input image file path
        input_path = "temp2.png"
        save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")])
        # Get input values from the input boxes
        incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_treshold = int(lower_treshold_input.get()) #lower treshold
        upper_treshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        outline = int(outline_input.get()) #outline thickness
        vertices = int(vertices_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        reduction_factor = 4
        if not input_path:
            print("No input file selected")
            return

        # get the current state of the checkbox
        
        # Load the image and convert it to grayscale
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply reduction factor
        gray_reduced = gray[::reduction_factor, ::reduction_factor]
        # Create a path for each line that contains black pixels

        # Load the input image
        img = cv2.imread(input_path, 1)
        img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
        thr = np.zeros_like(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray)
        # Increase the contrast of the grayscale image
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        cv2.blur(img, (1, 1), img)
        thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)
        contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None] * len(contours)

        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, vertices, True)
            if len(contours_poly[i]) > edge_complexity:
                cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
            else:
                cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))
        # Show the original image with contours overlaid
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.show()
       
        # Generate SVG file
        with open(save_svg_path, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            f.write(f'<svg width="{gray.shape[1]}" height="{gray.shape[0]}" viewBox="0 0 {gray.shape[1]} {gray.shape[0]}" xmlns="http://www.w3.org/2000/svg">\n')
            f.write('<style>path {stroke: black; stroke-width: 1; fill: none;}</style>\n') # add style for paths
            
            for y in range(gray_reduced.shape[0]):
                line = gray_reduced[y]
                black_pixels = [x for x in range(len(line)) if line[x] < upper_treshold]
                if len(line) >= 3:  # add check to ensure that contour has at least two points
                    if len(black_pixels) > 0:
                        y_original = y * reduction_factor
                        path = f'<path d="M {black_pixels[0]*reduction_factor} {y_original} '
                        for i in range(1, len(black_pixels)):
                            if black_pixels[i] == black_pixels[i-1] + 1:
                                path += f'L {black_pixels[i]*reduction_factor} {y_original} '
                            else:
                                f.write(f'{path}" />\n')
                                path = f'<path d="M {black_pixels[i]*reduction_factor} {y_original} '
                        f.write(f'{path}" />\n')

            for i, contour in enumerate(contours_poly):
                if len(contour) >= 2:  # add check to ensure that contour has at least two points
                    path_string = 'M '
                    for point in contour.squeeze():
                        path_string += '{},{} '.format(point[0], point[1])
                    path_string += 'Z '
                    f.write(f'<path d="{path_string}" />\n') # remove stroke and stroke-width attributes

            f.write('</svg>')
        print("SVG file saved successfully")
    
    def Image_to_svg_diagonal():
        # Ask for the input image file path
        #input_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        input_path = "temp2.png"
        save_svg_path = asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Image", "*.svg")])
        # Get input values from the input boxes
        incrase_resolution = float(incrase_resolution_input.get()) #scale up input image
        lower_treshold = int(lower_treshold_input.get()) #lower treshold
        upper_treshold = int(upper_treshold_input.get())
        edge_complexity = int(edge_complexity_input.get()) #complexity of line --> lower is higher complexity
        contour_range = int(contour_range_input.get())
        outline = int(outline_input.get()) #outline thickness
        vertices = int(vertices_input.get()) #outline thickness
        alpha =  float(alpha_input1.get()) # contrast multiplier
        beta = float(beta_input.get())  # shift factor
        contour_loops=int(contour_loops_input.get())
        color_loops_1=int(color_loops_1_input.get())
        color_loops_2=int(color_loops_2_input.get())
        color_loops_3=int(color_loops_3_input.get())
        color_loops_4=int(color_loops_4_input.get())
        color_loops_5=int(color_loops_5_input.get())
        color_loops_6=int(color_loops_6_input.get())
        color_loops_horizontal=int(color_loops_horizontal_input.get())
        
        # get the current state of the checkbox for contours  
        #reduction_factor = int(reduction_factor_entry.get())
        
        reduction_factor=int(reduction_factor_input.get())
        
        
        
        if not input_path:
            print("No input file selected")
            return
        # Load the image and convert it to grayscale
        img = cv2.imread(input_path)
        img = cv2.resize(img, None, fx=incrase_resolution, fy=incrase_resolution, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rows, cols = gray.shape
        angle = 0
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        gray = cv2.warpAffine(gray, M, (cols, rows))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Convert the image to PIL format
        img2 = img 
        img2= Image.fromarray(gray)

        # Reduce the number of colors to 5 using adaptive palette method
        out = img2.convert('P', palette=Image.ADAPTIVE, colors=6)
        # Display the image
        out_photo = ImageTk.PhotoImage(out)
        # Create the canvas image item and store its ID
        # Create Tkinter PhotoImage object with new image
     

        # Update the PhotoImage object held by the label widget
        label.configure(image=out_photo)
        label.image = out_photo  # Store a reference to prevent garbage collection

        # Update the scroll region of the canvas to include the new image size
        canvas.config(scrollregion=canvas.bbox("all"))
        out.save('temp4.png')

        
        #load reduced image
        imgl = cv2.imread('temp4.png')
        gray_reduced = imgl[::int(reduction_factor), ::int(reduction_factor)]
        # Get the palette of the image
        palette = out.getpalette()
        
        # Find the darkest to the lightest color in the palette
        colors = []
        for i in range(0, 6):
            color_index = i * 3
            color = (palette[color_index], palette[color_index + 1], palette[color_index + 2])
            colors.append(color)
        
        
        # Print the list of colors from darkest to lightest
        print("Colors (darkest to lightest):")
        for color in colors:
            print(color)

        # Create a path for each line that contains black pixels
        thr = np.zeros_like(gray_reduced)
        # Increase the contrast of the grayscale image
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        thr = cv2.Canny(gray, lower_treshold, upper_treshold, None, 3, False)
        contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None] * len(contours)

        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, vertices, True)
            if len(contours_poly[i]) > edge_complexity:
                cv2.drawContours(img, contours_poly, i, (0, 255, 0), outline, 8, hierarchy, 0, (0, 0))
            else:
                cv2.drawContours(img, contours_poly, i, (0, 0, 255), outline, 8, hierarchy, 0, (0, 0))

        # Generate SVG file
        with open(save_svg_path, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            f.write(f'<svg width="{gray.shape[1]}" height="{gray.shape[0]}" viewBox="0 0 {gray.shape[1]} {gray.shape[0]}" xmlns="http://www.w3.org/2000/svg">\n')
            f.write('<style>path {stroke: black; stroke-width: 1; fill: none;}</style>\n') # add style for paths
            for x in range(gray_reduced.shape[0]):
                for i in range(color_loops_6):  
                    #DARKEST GRAY SHADE 6/6 (color 0 to 5)
                    line2 = gray_reduced[x]
                    black_pixels2 = [y for y in range(len(line2)) if (line2[y] == colors[5][0]).all()]
                    print(f"Length of black_pixels for line2 {x}: {len(black_pixels2)}")

                    if len(line2) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels2) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels2[0]*reduction_factor} {x_original} '
                            for i in range(1, len(black_pixels2)):
                                if black_pixels2[i] == black_pixels2[i-1] + 1:
                                    path += f'L {black_pixels2[i]*reduction_factor} {x_original} '
                                else:
                                    f.write(f'{path}" />\n')
                                    path = f'<path d="M {black_pixels2[i]*reduction_factor} {x_original} '
                            f.write(f'{path}" />\n')  
                            update_progress()


                        
                         
                for i in range(color_loops_5):                 
                    line = gray_reduced[x]
                    black_pixels = [y for y in range(len(line)) if (line[y] == colors[4][0]).all()]
                    print(f"Length of black_pixels for line {x}: {len(black_pixels)}")
                    # 3rd DARKEST SHADE 4/6 (color 0 to 5)
                    if len(line) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels[0]*reduction_factor} {x_original} '
                            dashed = False  # set the flag to indicate if the current segment is dashed
                            segment_length = 0  # initialize the length of the current segment
                            for i in range(1, len(black_pixels)):
                                if black_pixels[i] == black_pixels[i-1] + 1:  # if the pixels are consecutive
                                    if not dashed and segment_length < 5:  # if the current segment is not dashed and the length is less than 10
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    elif dashed and segment_length < 5:  # if the current segment is dashed and the length is less than 5
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    else:  # if the current segment should be dashed
                                        dashed = not dashed  # toggle the flag
                                        path += f'" stroke-dasharray="5 1" />\n'  # add the path with the dashed stroke
                                        path += f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                                        segment_length = 0  # reset the length of the segment
                                    segment_length += 1  # increment the length of the segment
                                else:  # if the pixels are not consecutive
                                    dashed = False  # reset the flag
                                    segment_length = 0  # reset the length of the segment
                                    f.write(f'{path}" />\n')  # add the current path to the file
                                    path = f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                            f.write(f'{path}" />\n')  # add the last path to the file              
                            update_progress()
                        
                        
                for i in range(color_loops_4):        
                    # Medium GRAY SHADE 3/6 (color 0 to 5)
                    line = gray_reduced[x]
                    black_pixels = [y for y in range(len(line)) if (line[y] == colors[3][0]).all()]
                    print(f"Length of black_pixels for line {x}: {len(black_pixels)}")
                    update_progress()
                    if len(line) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels[0]*reduction_factor} {x_original} '
                            dashed = False  # set the flag to indicate if the current segment is dashed
                            segment_length = 0  # initialize the length of the current segment
                            for i in range(1, len(black_pixels)):
                                if black_pixels[i] == black_pixels[i-1] + 1:  # if the pixels are consecutive
                                    if not dashed and segment_length < 3:  # if the current segment is not dashed and the length is less than 10
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    elif dashed and segment_length < 3:  # if the current segment is dashed and the length is less than 5
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    else:  # if the current segment should be dashed
                                        dashed = not dashed  # toggle the flag
                                        path += f'" stroke-dasharray="3 3" />\n'  # add the path with the dashed stroke
                                        path += f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                                        segment_length = 0  # reset the length of the segment
                                    segment_length += 1  # increment the length of the segment
                                else:  # if the pixels are not consecutive
                                    dashed = False  # reset the flag
                                    segment_length = 0  # reset the length of the segment
                                    f.write(f'{path}" />\n')  # add the current path to the file
                                    path = f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                            f.write(f'{path}" />\n')  # add the last path to the file
                            update_progress()
                        
                        
                        
                for i in range(color_loops_3):     
                    line = gray_reduced[x]
                    black_pixels = [y for y in range(len(line)) if (line[y] == colors[2][0]).all()]
                    print(f"Length of black_pixels for line {x}: {len(black_pixels)}")
                    # Light GRAY SHADE 2/6 (color 0 to 5)
                    if len(line) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels[0]*reduction_factor} {x_original} '
                            dashed = False  # set the flag to indicate if the current segment is dashed
                            segment_length = 0  # initialize the length of the current segment
                            for i in range(1, len(black_pixels)):
                                if black_pixels[i] == black_pixels[i-1] + 1:  # if the pixels are consecutive
                                    if not dashed and segment_length < 2:  # if the current segment is not dashed and the length is less than 10
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    elif dashed and segment_length < 2:  # if the current segment is dashed and the length is less than 5
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    else:  # if the current segment should be dashed
                                        dashed = not dashed  # toggle the flag
                                        path += f'" stroke-dasharray="2 8" />\n'  # add the path with the dashed stroke
                                        path += f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                                        segment_length = 0  # reset the length of the segment
                                    segment_length += 1  # increment the length of the segment
                                else:  # if the pixels are not consecutive
                                    dashed = False  # reset the flag
                                    segment_length = 0  # reset the length of the segment
                                    f.write(f'{path}" />\n')  # add the current path to the file
                                    path = f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                            f.write(f'{path}" />\n')  # add the last path to the file
                            update_progress()
                        
                        
                        
                for i in range(color_loops_2):        
                    # white 1/6 (color 0 to 5)
                    line = gray_reduced[x]
                    black_pixels = [y for y in range(len(line)) if (line[y] == colors[1][0]).all()]
                    print(f"Length of black_pixels for line {x}: {len(black_pixels)}")

                    if len(line) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels[0]*reduction_factor} {x_original} '
                            dashed = False  # set the flag to indicate if the current segment is dashed
                            segment_length = 0  # initialize the length of the current segment
                            for i in range(1, len(black_pixels)):
                                if black_pixels[i] == black_pixels[i-1] + 1:  # if the pixels are consecutive
                                    if not dashed and segment_length < 2:  # if the current segment is not dashed and the length is less than 10
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    elif dashed and segment_length < 2:  # if the current segment is dashed and the length is less than 5
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    else:  # if the current segment should be dashed
                                        dashed = not dashed  # toggle the flag
                                        path += f'" stroke-dasharray="2 16" />\n'  # add the path with the dashed stroke
                                        path += f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                                        segment_length = 0  # reset the length of the segment
                                    segment_length += 1  # increment the length of the segment
                                else:  # if the pixels are not consecutive
                                    dashed = False  # reset the flag
                                    segment_length = 0  # reset the length of the segment
                                    f.write(f'{path}" />\n')  # add the current path to the file
                                    path = f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                            f.write(f'{path}" />\n')  # add the last path to the file
                            update_progress()
                        
                        
                for i in range(color_loops_1):        
                    line = gray_reduced[x]
                    black_pixels = [y for y in range(len(line)) if (line[y] == colors[0][0]).all()]
                    print(f"Length of black_pixels for line {x}: {len(black_pixels)}")
                    if len(line) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels) > 0:
                            x_original = x * reduction_factor
                            path = f'<path d="M {black_pixels[0]*reduction_factor} {x_original} '
                            dashed = False  # set the flag to indicate if the current segment is dashed
                            segment_length = 0  # initialize the length of the current segment
                            for i in range(1, len(black_pixels)):
                                if black_pixels[i] == black_pixels[i-1] + 1:  # if the pixels are consecutive
                                    if not dashed and segment_length < 3:  # if the current segment is not dashed and the length is less than 10
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    elif dashed and segment_length < 3:  # if the current segment is dashed and the length is less than 5
                                        path += f'L {black_pixels[i]*reduction_factor} {x_original} '  # add the pixel to the path
                                    else:  # if the current segment should be dashed
                                        dashed = not dashed  # toggle the flag
                                        path += f'" stroke-dasharray="0 100" />\n'  # add the path with the dashed stroke
                                        path += f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                                        segment_length = 0  # reset the length of the segment
                                    segment_length += 1  # increment the length of the segment
                                else:  # if the pixels are not consecutive
                                    dashed = False  # reset the flag
                                    segment_length = 0  # reset the length of the segment
                                    f.write(f'{path}" />\n')  # add the current path to the file
                                    path = f'<path d="M {black_pixels[i]*reduction_factor} {x_original} '  # start a new path with a solid stroke
                            f.write(f'{path}" />\n')  # add the last path to the file
                            update_progress()             



            for i in range(color_loops_horizontal):    
                for y in range(gray_reduced.shape[1]):

                    #DARKEST GRAY SHADE 6/6 (color 0 to 5)
                    line2 = gray_reduced[:, y]
                    black_pixels2 = [x for x in range(len(line2)) if (line2[x] == colors[5][0]).all()]


                    if len(line2) >= 3:  # add check to ensure that contour has at least two points
                        if len(black_pixels2) > 0:
                            y_original = y * reduction_factor
                            path = f'<path d="M {y_original} {black_pixels2[0]*reduction_factor} '
                            for i in range(1, len(black_pixels2)):
                                if black_pixels2[i] == black_pixels2[i-1] + 1:
                                    path += f'L {y_original} {black_pixels2[i]*reduction_factor} '
                                else:
                                
                                    f.write(f'{path}" />\n')
                                    path = f'<path d="M {y_original} {black_pixels2[i]*reduction_factor} '
                            f.write(f'{path}" />\n')
                            update_progress()


           
            
            for i in range(contour_loops):
                for i, contour in enumerate(contours_poly):
                    if len(contour) >= 2:  # add check to ensure that contour has at least two points
                        path_string = 'M '
                        for point in contour.squeeze():
                            path_string += '{},{} '.format(point[0], point[1])
                        path_string += 'Z '
                        f.write(f'<path d="{path_string}" />\n') # remove stroke and stroke-width attributes
                        update_progress()
            
            f.write('</svg>')
        print("SVG file saved successfully")
        


    # Checkboxes
    #var1 = tk.IntVar()
    #c1 = tk.Checkbutton(window, text='Python',variable=var1, onvalue=1, offvalue=0)
    #c1.grid(row=16, column=0, padx=5, pady=5, sticky="W")
    
    # Create labels for the input boxes
    incrase_resolution_label = ttk.Label(window, text="Increase Resolution")
    lower_treshold_label = ttk.Label(window, text="Lower Threshold")
    upper_treshold_label = ttk.Label(window, text="Upper Threshold")
    edge_complexity_label = ttk.Label(window, text="Edge Complexity")
    contour_range_label = ttk.Label(window, text="Contour Range")
    outline_label = ttk.Label(window, text="Outline")
    vertices_label = ttk.Label(window, text="Vertices")
    alpha_input1_label = ttk.Label(window, text="Alpha/Blur")
    beta_input_label = ttk.Label(window, text="Contrastt")
    optimize_tres_input_label = ttk.Label(window, text="svg optimizer treshold")
    minLineL_input_label = ttk.Label(window, text="minimum line lenght")
    LineGap_input_label = ttk.Label(window, text="maximum line Gap")
    particle_density_input_label = ttk.Label(window, text="particle density")
    particle_density_edges_input_label = ttk.Label(window, text="particle density EDGES")
    particle_distance_input_label = ttk.Label(window, text="particle DISTANCE")     
    particle_connections_input_label = ttk.Label(window, text="particle connection lines")
    contour_loops_input_label = ttk.Label(window, text="contour passes (0 or 1)")
    color_loops_1_input_label = ttk.Label(window, text="color 1 passes")
    color_loops_2_input_label = ttk.Label(window, text="color 2 passes")
    color_loops_3_input_label = ttk.Label(window, text="color 3 passes")
    color_loops_4_input_label = ttk.Label(window, text="color 4 passes")
    color_loops_5_input_label = ttk.Label(window, text="color 5 passes")
    color_loops_6_input_label = ttk.Label(window, text="color 6 passes")
    color_loops_horizontal_input_label= ttk.Label(window, text="horizontal line passes")
    reduction_factor_input_label= ttk.Label(window, text="line reduction factor")
    vectorimagesettings= ttk.Label(window, text="Vector Pattern Settings")
    
    progress_bar = ttk.Progressbar(window, orient="horizontal", mode="determinate", length=300)
    # Set the maximum value of the progress bar
    progress_bar["maximum"] = 100
    

    # Create input boxes for parameters
    incrase_resolution_input = ttk.Entry(window)
    incrase_resolution_input.insert(0, "1")
    lower_treshold_input = ttk.Entry(window)
    lower_treshold_input.insert(0, "50")
    upper_treshold_input = ttk.Entry(window)
    upper_treshold_input.insert(0, "190")
    edge_complexity_input = ttk.Entry(window)
    edge_complexity_input.insert(0, "1")
    contour_range_input = ttk.Entry(window)
    contour_range_input.insert(0, "2")
    outline_input = ttk.Entry(window)
    outline_input.insert(0, "1")
    vertices_input = ttk.Entry(window)
    vertices_input.insert(0, "1")
    alpha_input1 = ttk.Entry(window)
    alpha_input1.insert(0, "1.0")
    beta_input = ttk.Entry(window)
    beta_input.insert(0, "0")
    optimize_tres_input = ttk.Entry(window)
    optimize_tres_input.insert(0, "10")
    minLineL_input=ttk.Entry(window)
    minLineL_input.insert(0, "10")                              
    LineGap_input=ttk.Entry(window)
    LineGap_input.insert(0, "5")
    particle_density_input=ttk.Entry(window)
    particle_density_input.insert(0, "1")
    particle_density_edges_input=ttk.Entry(window)
    particle_density_edges_input.insert(0, "1")
    particle_distance_input=ttk.Entry(window)
    particle_distance_input.insert(0, "100")
    particle_connections_input= ttk.Entry(window)
    particle_connections_input.insert(0, "5")
    contour_loops_input= ttk.Entry(window)
    contour_loops_input.insert(0, "1")
    color_loops_1_input= ttk.Entry(window)
    color_loops_1_input.insert(0, "1")
    color_loops_2_input= ttk.Entry(window)
    color_loops_2_input.insert(0, "1")
    color_loops_3_input= ttk.Entry(window)
    color_loops_3_input.insert(0, "1")
    color_loops_4_input= ttk.Entry(window)
    color_loops_4_input.insert(0, "1")
    color_loops_5_input= ttk.Entry(window)
    color_loops_5_input.insert(0, "1")
    color_loops_6_input= ttk.Entry(window)
    color_loops_6_input.insert(0, "1")
    color_loops_horizontal_input= ttk.Entry(window)
    color_loops_horizontal_input.insert(0, "1")
    reduction_factor_input= ttk.Entry(window)
    reduction_factor_input.insert(0, "4")
    
    
    
    
    
    
    
    
    
    # Create run buttons
    svg_button = ttk.Button(window, text="contours to  SVG", command=run_imagevector)
    export_optimized = ttk.Button(window, text="optimized contours to SVG", command=optimized_imagevector)
    export_png = ttk.Button(window, text="Treshold outlines to PNG", command=png_save)
    line_to_svg_button = ttk.Button(window, text="Image to Sribble SVG", command=run_linevector)
    particle_density_button = ttk.Button(window, text="Image Triangulate SVG", command=run_particle)
    image_to_particle__button = ttk.Button(window, text="Image to particle", command=Image_to_Particle)
    image_to_svg_button = ttk.Button(window, text="Shades to SVG", command=Image_to_svg)
    image_to_svg_diagonal_button = ttk.Button(window, text="Image to 6 Shades SVG", command=Image_to_svg_diagonal)
    cleanup_svg_button = ttk.Button(window, text="cleanup SVG", command=cleanup_svg)
    svg_trace_button=ttk.Button(window, text="SVG Trace", command=svg_trace)
    svg_to_png_button = ttk.Button(window, text=" SVG to PNG", command=svg_to_png)
    load_image_button = ttk.Button(window, text=" Load Image", command=load_image)
    # Arrange the labels and input boxes into a block using grid
    incrase_resolution_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")
    incrase_resolution_input.grid(row=0, column=1, padx=5, pady=5, sticky="E")
    lower_treshold_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")
    lower_treshold_input.grid(row=1, column=1, padx=5, pady=5, sticky="E")
    upper_treshold_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
    upper_treshold_input.grid(row=2, column=1, padx=5, pady=5, sticky="E")
    edge_complexity_label.grid(row=3, column=0, padx=5, pady=5, sticky="W")
    edge_complexity_input.grid(row=3, column=1, padx=5, pady=5, sticky="E")
    contour_range_label.grid(row=4, column=0, padx=5, pady=5, sticky="W")
    contour_range_input.grid(row=4, column=1, padx=5, pady=5, sticky="E")
    outline_label.grid(row=5, column=0, padx=5, pady=5, sticky="W")
    outline_input.grid(row=5, column=1, padx=5, pady=5, sticky="E")
    vertices_label.grid(row=6, column=0, padx=5, pady=5, sticky="W")
    vertices_input.grid(row=6, column=1, padx=5, pady=5, sticky="E")
    alpha_input1_label.grid(row=7, column=0, padx=5, pady=5, sticky="W")
    alpha_input1.grid(row=7, column=1, padx=5, pady=5, sticky="E")
    beta_input_label.grid(row=8, column=0, padx=5, pady=5, sticky="W")
    beta_input.grid(row=8, column=1, padx=5, pady=5, sticky="E")
    optimize_tres_input_label.grid(row=9, column=0, padx=5, pady=5, sticky="W")
    optimize_tres_input.grid(row=9, column=1, padx=5, pady=5, sticky="E")
    minLineL_input_label.grid(row=10, column=0, padx=5, pady=5, sticky="W")
    minLineL_input.grid(row=10, column=1, padx=5, pady=5, sticky="E")
    LineGap_input_label.grid(row=11, column=0, padx=5, pady=5, sticky="W")
    LineGap_input.grid(row=11, column=1, padx=5, pady=5, sticky="E")
    particle_density_input_label.grid(row=12, column=0, padx=5, pady=5, sticky="W")
    particle_density_input.grid(row=12, column=1, padx=5, pady=5, sticky="E")
    particle_density_edges_input_label.grid(row=13, column=0, padx=5, pady=5, sticky="W")
    particle_density_edges_input.grid(row=13, column=1, padx=5, pady=5, sticky="E")
    particle_distance_input_label.grid(row=14, column=0, padx=5, pady=5, sticky="W")
    particle_distance_input.grid(row=14, column=1, padx=5, pady=5, sticky="E")
    particle_connections_input_label.grid(row=15, column=0, padx=5, pady=5, sticky="W")
    particle_connections_input.grid(row=15, column=1, padx=5, pady=5, sticky="E")
    
    load_image_button.grid(row=0, column=4, padx=5, pady=5, sticky="W")
    vectorimagesettings.grid(row=0, column=3, padx=5, pady=5, sticky="W")
    reduction_factor_input_label.grid(row=1, column=3, padx=5, pady=5, sticky="W")
    reduction_factor_input.grid(row=1, column=4, padx=5, pady=5, sticky="E")
    contour_loops_input_label.grid(row=2, column=3, padx=5, pady=5, sticky="W")
    contour_loops_input.grid(row=2, column=4, padx=5, pady=5, sticky="E")
    color_loops_1_input_label.grid(row=3, column=3, padx=5, pady=5, sticky="W")
    color_loops_1_input.grid(row=3, column=4, padx=5, pady=5, sticky="E")
    color_loops_2_input_label.grid(row=4, column=3, padx=5, pady=5, sticky="W")
    color_loops_2_input.grid(row=4, column=4, padx=5, pady=5, sticky="E")
    color_loops_3_input_label.grid(row=5, column=3, padx=5, pady=5, sticky="W")
    color_loops_3_input.grid(row=5, column=4, padx=5, pady=5, sticky="E")
    color_loops_4_input_label.grid(row=6, column=3, padx=5, pady=5, sticky="W")
    color_loops_4_input.grid(row=6, column=4, padx=5, pady=5, sticky="E")
    color_loops_5_input_label.grid(row=7, column=3, padx=5, pady=5, sticky="W")
    color_loops_5_input.grid(row=7, column=4, padx=5, pady=5, sticky="E")
    color_loops_6_input_label.grid(row=8, column=3, padx=5, pady=5, sticky="W")
    color_loops_6_input.grid(row=8, column=4, padx=5, pady=5, sticky="E")
    color_loops_horizontal_input_label.grid(row=9, column=3, padx=5, pady=5, sticky="W")
    color_loops_horizontal_input.grid(row=9, column=4, padx=1, pady=1, sticky="E")
    image_to_svg_diagonal_button.grid(row=10, column=4, padx=5, pady=5, sticky="W")
    
    # Arrange the buttons
    svg_button.grid(row=24, column=0, padx=5, pady=5, sticky="W")
    export_optimized.grid(row=24, column=1, padx=5, pady=5, sticky="E")
    export_png.grid(row=25, column=0, padx=5, pady=5, sticky="W")
    line_to_svg_button.grid(row=25, column=1, padx=5, pady=5, sticky="E") 
    particle_density_button.grid(row=26, column=0, padx=5, pady=5, sticky="W")
    image_to_particle__button.grid(row=27, column=0, padx=5, pady=5, sticky="W")
    image_to_svg_button.grid(row=28, column=0, padx=5, pady=5, sticky="W")
    svg_trace_button.grid(row=28, column=1, padx=5, pady=5, sticky="E")
    cleanup_svg_button.grid(row=29, column=0, padx=5, pady=5, sticky="W")
    # Pack the progress bar widget
    progress_bar.grid(row=31, column=0, columnspan=2, padx=1, pady=1, sticky="W")
    svg_to_png_button.grid(row=29, column=1, padx=5, pady=5, sticky="W")

    
    # Bind function to handle window close event
    def on_closing():
        win.destroy()
        window.destroy()

    win = tk.Toplevel()
    win.title("MECHANICUS_V.0.1 Beta")
    win.configure(bg="#263d42", borderwidth=0)
    
    # Open image file
    img = Image.open("temp2.png")

    # Create Tkinter PhotoImage object
    photo = ImageTk.PhotoImage(img)

    # Create a canvas widget and add it to the window
    #canvas = tk.Canvas(win, width=img.width, height=img.height)
    canvas = tk.Canvas(win, width=1000, height=600)
    canvas.grid(row=1, column=0, padx=5, pady=5)

    # Create horizontal and vertical scrollbars for the canvas
    hbar = tk.Scrollbar(win, orient=tk.HORIZONTAL, command=canvas.xview)
    hbar.grid(row=2, column=0, sticky="we")
    vbar = tk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
    vbar.grid(row=1, column=1, sticky="ns")
    canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    # Create a label widget to hold the image and add it to the canvas
    label = tk.Label(canvas, image=photo)
    label.image = photo  # Store a reference to prevent garbage collection
    canvas.create_window(0, 0, anchor="nw", window=label)
    
    # Set the scrollable area
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind function to handle window close event
    win.protocol("WM_DELETE_win", on_closing)

    # Run GUI loop
    win.mainloop()
    window.mainloop()

#Imagevector()
