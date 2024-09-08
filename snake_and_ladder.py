import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk, ImageDraw
import time
import math
import os  # Import the os module

class SnakeAndLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Snake and Ladder Game')
        self.root.iconbitmap('snake.ico')

        self.board_size = 10
        self.cell_size = 60
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(side=tk.LEFT)
        
        self.info_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.snakes = {25: 6, 47: 26, 49: 10, 56: 53, 62: 17, 64: 58, 87: 24, 93: 63, 95: 3, 98: 78}
        self.ladders = {2: 38, 4: 14, 9: 31, 21: 42, 27: 84, 36: 44, 51: 86, 71: 91, 80: 100}

        # Define the player information
        self.player_positions = {'P1': 0, 'P2': 0}
        self.current_player = 'P1'
        self.player_colors = {'P1': '#FF5722', 'P2': '#2196F3'}

        self.canvas = tk.Canvas(self.board_frame, width=self.board_size * self.cell_size,
                                height=self.board_size * self.cell_size)
        self.canvas.pack()

        # Get the current directory of the script
        self.current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script directory

        self.load_images()
        self.create_board()
        self.create_info_panel()
        self.create_players()

    def load_images(self):
        self.dice_images = []
        for i in range(1, 7):
            try:
                dice_path = os.path.join(self.current_dir, f"dice{i}.png")  # Construct the dynamic path
                self.dice_images.append(ImageTk.PhotoImage(Image.open(dice_path).resize((50, 50))))
            except FileNotFoundError:
                print(f"Warning: dice{i}.png not found. Using default dice face.")
                self.dice_images.append(self.create_dice_face(i))

        try:
            snake_path = os.path.join(self.current_dir, "snake.png")  # Construct the dynamic path for snake.png
            self.snake_image = ImageTk.PhotoImage(Image.open(snake_path).resize((50, 50)))
        except FileNotFoundError:
            print("Warning: snake.png not found. Using default snake head.")
            self.snake_image = None

    def create_colored_rectangle(self, size, color):
        img = Image.new('RGB', size, color)
        return ImageTk.PhotoImage(img)

    def create_dice_face(self, number):
        size = (50, 50)
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw black border
        draw.rectangle([0, 0, 49, 49], outline='black')
        
        # Draw dots based on the number
        dots = {
            1: [(25, 25)],
            2: [(15, 15), (35, 35)],
            3: [(15, 15), (25, 25), (35, 35)],
            4: [(15, 15), (15, 35), (35, 15), (35, 35)],
            5: [(15, 15), (15, 35), (25, 25), (35, 15), (35, 35)],
            6: [(15, 15), (15, 25), (15, 35), (35, 15), (35, 25), (35, 35)]
        }
        
        for dot in dots[number]:
            draw.ellipse([dot[0]-3, dot[1]-3, dot[0]+3, dot[1]+3], fill='black')
        
        return ImageTk.PhotoImage(img)

    def create_board(self):
        self.cells = []
        for row in range(self.board_size):
            row_cells = []
            for col in range(self.board_size):
                cell_number = (self.board_size * self.board_size) - (row * self.board_size + col)
                cell_color = '#E6F3FF' if (row + col) % 2 == 0 else '#B3D9FF'
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline='#4D4D4D')
                self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, 
                                        text=str(cell_number), font=('Arial', 10, 'bold'))
                row_cells.append((x1, y1, x2, y2))
            self.cells.append(row_cells)
        
        self.draw_snakes_and_ladders()

    def draw_snakes_and_ladders(self):
        for start, end in self.snakes.items():
            self.draw_snake(start, end)
        for start, end in self.ladders.items():
            self.draw_ladder(start, end)

    def draw_snake(self, start, end):
        start_pos = self.get_cell_center(start)
        end_pos = self.get_cell_center(end)
        
        # Generate curvy snake body
        points = self.generate_curve(start_pos, end_pos)
        
        # Draw enhanced snake body
        self.draw_enhanced_snake_body(points)
        
        # Draw snake head using the image
        if self.snake_image:
            self.canvas.create_image(start_pos[0], start_pos[1], image=self.snake_image, anchor=tk.CENTER)
        else:
            # Fallback to drawing an oval if the image is not available
            head_size = 25
            self.canvas.create_oval(start_pos[0]-head_size, start_pos[1]-head_size, 
                                    start_pos[0]+head_size, start_pos[1]+head_size, 
                                    fill='#388E3C', outline='#1B5E20', width=2)
        
        # Draw enhanced snake tail
        self.draw_enhanced_snake_tail(points[-3:])

    def draw_enhanced_snake_body(self, points):
        # Draw main body
        self.canvas.create_line(points, fill='#4CAF50', width=9, smooth=True, splinesteps=36)
        
        # Draw body pattern
        pattern_points = self.generate_pattern_points(points)
        self.canvas.create_line(pattern_points, fill='#81C784', width=4, smooth=True, splinesteps=36, dash=(3, 3))

    def generate_pattern_points(self, points):
        pattern_points = []
        for i in range(0, len(points) - 1, 2):
            x1, y1 = points[i]
            x2, y2 = points[i + 1] if i + 1 < len(points) else points[i]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            pattern_points.extend([x1, y1, mid_x, mid_y])
        return pattern_points

    def draw_enhanced_snake_tail(self, tail_points):
        # Draw a tapered tail
        tail_width = 12
        for i in range(len(tail_points) - 1):
            x1, y1 = tail_points[i]
            x2, y2 = tail_points[i + 1]
            tail_width = max(1, tail_width - 3)  # Ensure the width doesn't go below 1
            self.canvas.create_line(x1, y1, x2, y2, fill='#4CAF50', width=tail_width, capstyle=tk.ROUND)

    def generate_curve(self, start, end):
        points = [start]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx*dx + dy*dy)
        steps = int(distance / 30)  # Adjust this value to change the curviness
        
        for i in range(1, steps):
            t = i / steps
            x = start[0] + dx * t + random.randint(-20, 20)
            y = start[1] + dy * t + random.randint(-20, 20)
            points.append((x, y))
        
        points.append(end)
        return points

    def draw_ladder(self, start, end):
        start_pos = self.get_cell_center(start)
        end_pos = self.get_cell_center(end)
        self.canvas.create_line(start_pos[0]-10, start_pos[1], end_pos[0]-10, end_pos[1], 
                                fill='#8D6E63', width=5)
        self.canvas.create_line(start_pos[0]+10, start_pos[1], end_pos[0]+10, end_pos[1], 
                                fill='#8D6E63', width=5)
        # Draw rungs
        steps = 5
        for i in range(steps):
            x1 = start_pos[0] - 10 + (end_pos[0] - start_pos[0]) * i / steps
            y1 = start_pos[1] + (end_pos[1] - start_pos[1]) * i / steps
            x2 = x1 + 20
            y2 = y1
            self.canvas.create_line(x1, y1, x2, y2, fill='#A1887F', width=3)

    def get_cell_center(self, cell_number):
        row, col = divmod(self.board_size * self.board_size - cell_number, self.board_size)
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        return (x, y)

    def create_info_panel(self):
        title_label = tk.Label(self.info_frame, text="Snake and Ladder", font=('Comic sans', 24, 'bold'), bg='#F0F0F0', fg='#1976D2')
        title_label.pack(pady=20)

        self.dice_button = self.create_styled_button("Roll Dice", self.roll_dice, self.player_colors['P1'])
        self.dice_button.pack(pady=20)
        
        self.dice_label = tk.Label(self.info_frame, image=self.dice_images[0], bg='#F0F0F0')
        self.dice_label.pack(pady=20)
        
        self.status_label = tk.Label(self.info_frame, text="Player 1's turn", 
                                     font=('Times New Roman', 16), bg='#F0F0F0', fg='#333333')
        self.status_label.pack(pady=20)
        
        self.p1_label = tk.Label(self.info_frame, text="Player 1 (Red): 0", 
                                 font=('Times New Roman', 14), bg='#F0F0F0', fg='#FF5722')
        self.p1_label.pack(pady=10)
        
        self.p2_label = tk.Label(self.info_frame, text="Player 2 (Blue): 0", 
                                 font=('Times New Roman', 14), bg='#F0F0F0', fg='#2196F3')
        self.p2_label.pack(pady=10)
        
        self.restart_button = self.create_styled_button("Restart Game", self.restart_game, '#2196F3')
        self.restart_button.pack(pady=20)
        
        self.quit_button = self.create_styled_button("Quit", self.root.quit, '#F44336')
        self.quit_button.pack(pady=20)

    def create_styled_button(self, text, command, bg_color):
        style = ttk.Style()
        style.configure(
            'RoundedButton.TButton',
            padding=10,
            relief="flat",
            background=bg_color,
            foreground="black",
            font=('Times New Roman', 16, 'italic')
        )
        style.map('RoundedButton.TButton',
                  background=[('active', self.adjust_color(bg_color, -20))],
                  relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        button = ttk.Button(self.info_frame, text=text, command=command, style='RoundedButton.TButton')
        return button


    @staticmethod
    def adjust_color(hex_color, amount):
        r = int(hex_color[1:3], 16) + amount
        g = int(hex_color[3:5], 16) + amount
        b = int(hex_color[5:7], 16) + amount
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        return f'#{r:02x}{g:02x}{b:02x}'

    def roll_dice(self):
        self.dice_button.config(state=tk.DISABLED)
        dice_value = random.randint(1, 6)
        self.animate_dice(dice_value)

    def animate_dice(self, final_value):
        for _ in range(10):  # Show 10 random dice faces
            random_value = random.randint(1, 6)
            self.dice_label.config(image=self.dice_images[random_value - 1])
            self.root.update()
            time.sleep(0.1)  # Slowed down animation
        
        self.dice_label.config(image=self.dice_images[final_value - 1])
        self.root.update()
        time.sleep(1)  # Pause to show final dice value
        
        self.move_player(final_value)


    def create_players(self):
        self.player_pieces = {
            'P1': self.canvas.create_oval(0, 0, 20, 20, fill=self.player_colors['P1'], outline='white'),
            'P2': self.canvas.create_oval(0, 0, 20, 20, fill=self.player_colors['P2'], outline='white')
        }
        self.update_player_positions()

    def update_player_positions(self):
        for player, position in self.player_positions.items():
            if position == 0:
                # Place player outside the board
                x, y = -30, self.board_size * self.cell_size / 2
                if player == 'P2':
                    x = self.board_size * self.cell_size + 30
            else:
                center = self.get_cell_center(position)
                x, y = center[0], center[1]
            
            self.canvas.coords(self.player_pieces[player], x-10, y-10, x+10, y+10)

    def move_player(self, steps):
        if self.player_positions[self.current_player] == 0 and steps != 1:
            self.status_label.config(text=f"{self.current_player} needs 1 to start")
            self.switch_player()
            self.dice_button.config(state=tk.NORMAL)
            return

        for _ in range(steps):
            self.player_positions[self.current_player] += 1
            if self.player_positions[self.current_player] > 100:
                self.player_positions[self.current_player] = 100
                break
            self.update_player_positions()
            self.update_labels()
            self.root.update()
            time.sleep(0.5)  # Slowed down movement
        
        self.check_snake_or_ladder()

    def check_snake_or_ladder(self):
        current_pos = self.player_positions[self.current_player]
        if current_pos in self.snakes:
            self.status_label.config(text=f"Oops! Snake! {self.current_player} moving from {current_pos} to {self.snakes[current_pos]}")
            self.root.update()
            time.sleep(1)  # Pause to show message
            self.animate_snake_movement(current_pos, self.snakes[current_pos])
            self.player_positions[self.current_player] = self.snakes[current_pos]
        elif current_pos in self.ladders:
            self.status_label.config(text=f"Yay! Ladder! {self.current_player} moving from {current_pos} to {self.ladders[current_pos]}")
            self.root.update()
            time.sleep(1)  # Pause to show message
            self.animate_ladder_movement(current_pos, self.ladders[current_pos])
            self.player_positions[self.current_player] = self.ladders[current_pos]
        
        self.update_player_positions()
        self.update_labels()
        
        if self.player_positions[self.current_player] == 100:
            self.status_label.config(text=f"Congratulations! {self.current_player} won!")
            self.dice_button.config(state=tk.DISABLED)
        else:
            self.switch_player()
            self.dice_button.config(state=tk.NORMAL)

    def switch_player(self):
        self.current_player = 'P2' if self.current_player == 'P1' else 'P1'
        self.status_label.config(text=f"{self.current_player}'s turn")
        self.dice_button.configure(style='RoundedButton.TButton')
        ttk.Style().configure('RoundedButton.TButton', background=self.player_colors[self.current_player])

    def update_labels(self):
        self.p1_label.config(text=f"Player 1 (Red): {self.player_positions['P1']}")
        self.p2_label.config(text=f"Player 2 (Blue): {self.player_positions['P2']}")

    def animate_snake_movement(self, start, end):
        start_pos = self.get_cell_center(start)
        end_pos = self.get_cell_center(end)
        points = self.generate_curve(start_pos, end_pos)
        
        for point in points:
            self.canvas.coords(self.player_pieces[self.current_player], point[0]-10, point[1]-10, point[0]+10, point[1]+10)
            self.root.update()
            time.sleep(0.1)  # Slowed down animation

    def animate_ladder_movement(self, start, end):
        start_pos = self.get_cell_center(start)
        end_pos = self.get_cell_center(end)
        
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
            self.canvas.coords(self.player_pieces[self.current_player], x-10, y-10, x+10, y+10)
            self.root.update()
            time.sleep(0.1)  # Slowed down animation

    def restart_game(self):
        self.player_positions = {'P1': 0, 'P2': 0}
        self.current_player = 'P1'
        self.update_player_positions()
        self.update_labels()
        self.status_label.config(text="Player 1's turn")
        self.dice_button.config(state=tk.NORMAL)
        self.dice_label.config(image=self.dice_images[0])

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeAndLadderGame(root)
    root.mainloop()