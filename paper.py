from typing import Tuple

import sys
import argparse

import reportlab.lib.pagesizes as pagesizes

from reportlab.pdfgen import canvas
from reportlab.lib import colors

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("paper")

def mult_floor(n: float, multiple: float) -> int:
    return int((n // multiple) * multiple)

def create_engineering_sheet(filename:str, margin: Tuple[float, float, float, float]=(30, 30, 30, 30),
                             grid_size:int=10, page_size: Tuple[float, float]=pagesizes.letter,
                             major_line_color: colors.Color=colors.darkgreen, major_line_thickness: float=0.5, major_line_interval=5,
                             minor_line_color: colors.Color=colors.lightgreen, minor_line_thickness: float=0.2,
                             border_line_color: colors.Color=colors.darkgreen, border_line_thickness: float=1.5,
                             background_color: colors.Color=colors.HexColor("#faf3bd"),
                             stretch_grid: bool=True, horizontal_center: bool=True, vertical_center: bool=True):
    # Create a canvas to write on
    c = canvas.Canvas(filename, pagesize=page_size)
    margin_top, margin_left, margin_bottom, margin_right = margin
    log.debug(f"Margins: {margin_top=}, {margin_right=}, {margin_bottom=}, {margin_left=}")
    # Get the width and height of the page
    width, height = page_size

    # Set background color by filling the entire page with a rectangle
    c.setFillColor(background_color)
    c.rect(0, 0, width, height, fill=1) 
   
    # calculate the number of vertical lines and number of horizontal lines that can fit inside the page
    num_vertical_spaces = (width - margin_left - margin_right) // grid_size
    num_horizontal_spaces = (height - margin_bottom - margin_top) // grid_size
    
    num_vertical_spaces = mult_floor(num_vertical_spaces, major_line_interval)
    num_horizontal_spaces = mult_floor(num_horizontal_spaces, major_line_interval)

    if stretch_grid:
        grid_size_vertical = (width - margin_left - margin_right) / num_vertical_spaces
        grid_size_horizontal = (height - margin_bottom - margin_top) / num_horizontal_spaces
        grid_size = min(grid_size_vertical, grid_size_horizontal)
        log.debug("adjusting grid size to %f", grid_size)
    
    top_stop = margin_bottom + num_horizontal_spaces * grid_size
    right_stop = margin_left + num_vertical_spaces * grid_size
    num_vertical_lines = num_vertical_spaces + 1
    num_horizontal_lines = num_horizontal_spaces + 1

    if horizontal_center:
        horizontal_delta = (width - margin_right - right_stop) / 2
        right_stop = right_stop + horizontal_delta
        margin_left = margin_left + horizontal_delta
        log.debug(f"horizontal_delta: {horizontal_delta}, right_stop: {right_stop}, margin_left: {margin_left}")
    if vertical_center:
        vertical_delta = (height - margin_top - top_stop) / 2
        top_stop = top_stop + vertical_delta
        margin_bottom = margin_bottom + vertical_delta

    # Draw the grid
    for axis, line_end, num_lines in [('x', top_stop, num_vertical_lines), ('y', right_stop, num_horizontal_lines)]:
        line_pos: float = margin_left if axis=='x' else margin_bottom        
        count = 0

        while count < num_lines:
            # Check if this is a major line (every 5 minor lines)
            if count % major_line_interval == 0:
                c.setStrokeColor(major_line_color)
                c.setLineWidth(major_line_thickness)
            else:
                c.setStrokeColor(minor_line_color)
                c.setLineWidth(minor_line_thickness)
            
            # Draw vertical or horizontal lines
            if axis == 'x':  # Vertical lines
                c.line(line_pos, margin_bottom, line_pos, line_end)
            else:  # Horizontal lines
                c.line(margin_left, line_pos, line_end, line_pos)
            
            # print(f"axis: {axis}, interval: {count % major_line_interval}, count: {count}, num_lines: {num_lines}, next_major: {next_major}, limit: {limit - margin_stop}, line_end: {line_end}, last_line_pos: {last_line_pos}")

            # Increment position and counter
            line_pos += grid_size
            count += 1

    # draw the border
    c.setStrokeColor(border_line_color)
    c.setLineWidth(border_line_thickness)
    c.line(margin_left, 0, margin_left, height)
    c.line(0, top_stop, width, top_stop)
    c.line(right_stop, 0, right_stop, height)
    c.line(margin_left, margin_bottom, right_stop, margin_bottom)

    # draw the thirds dividers on top
    thirds_spacing = (right_stop - margin_left)/3
    c.line(margin_left + thirds_spacing, top_stop, margin_left + thirds_spacing, height)
    c.line(margin_left + 2*thirds_spacing, top_stop, margin_left + 2*thirds_spacing, height)

    # Save the canvas to the file
    c.showPage()
    c.save()

# Usage
# create_engineering_sheet("custom_engineering_paper.pdf", margin=(30, 40, 30, 20), grid_size=12)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an PDF of engineering paper.")
    parser.add_argument("filename", type=str, help="The name of the output PDF file.")
    parser.add_argument("--margin", type=int, nargs=4, default=[30, 40, 30, 20], help="Margins for the sheet (top, left, bottom, right).")
    parser.add_argument("--grid_size", type=int, default=15, help="Size of the grid.")
    parser.add_argument("--page_size", type=str, default="letter", help="Size of the page.")
    parser.add_argument("--major_line_color", type=str, default="green", help="Color of the major lines.")
    parser.add_argument("--major_line_thickness", type=float, default=0.5, help="Thickness of the major lines.")
    parser.add_argument("--major_line_interval", type=int, default=5, help="Interval between major lines.")
    parser.add_argument("--minor_line_color", type=str, default="lightgreen", help="Color of the minor lines.")
    parser.add_argument("--minor_line_thickness", type=float, default=0.2, help="Thickness of the minor lines.")
    parser.add_argument("--border_line_color", type=str, default="darkgreen", help="Color of the border lines.")
    parser.add_argument("--border_line_thickness", type=float, default=1.5, help="Thickness of the border lines.")
    parser.add_argument("--background_color", type=str, default="#faf3bd", help="Background color of the sheet.")

    args = parser.parse_args()

    page_size = getattr(pagesizes, args.page_size)

    major_line_color = colors.toColor(args.major_line_color)
    minor_line_color = colors.toColor(args.minor_line_color)
    border_line_color = colors.toColor(args.border_line_color)
    background_color = colors.toColor(args.background_color)

    create_engineering_sheet(args.filename, margin=args.margin, 
                             grid_size=args.grid_size, page_size=page_size,
                             major_line_color=major_line_color, major_line_thickness=args.major_line_thickness, major_line_interval=args.major_line_interval,
                             minor_line_color=minor_line_color, minor_line_thickness=args.minor_line_thickness,
                             border_line_color=border_line_color, border_line_thickness=args.border_line_thickness,
                             background_color=background_color)
