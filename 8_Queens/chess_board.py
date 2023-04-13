import tkinter as tk
import python-chess

class ChessBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Board")
        self.canvas = tk.Canvas(self.root, width=320, height=320, bg="white")
        self.canvas.pack()

        self.draw_chess_board()

    def draw_chess_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * 40
                y1 = row * 40
                x2 = x1 + 40
                y2 = y1 + 40
                if (row + col) % 2 == 0:
                    color = "white"
                else:
                    color = "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

def main():
    root = tk.Tk()
    ChessBoard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
