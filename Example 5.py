from msilib import add_data
from tkinter import *
root=Tk()
root.title("Subtraction Calculator")
root.geometry('280x200')
entry1=Entry(root, bg="Light yellow",font=("Arial",12),justify=CENTER)
entry1.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
operation_label=Label(root,text="+",font=("Arial",14), bg="Light blue")
operation_label.grid(row=0,column=2,padx=10,pady=10)
entry2=Entry(root,bg="Light yellow",font=("Arial",12),justify=CENTER)
entry2.grid(row=0,column=3,columnspan=2,padx=10,pady=10)
def calculate_result():
    try:
        num1=float(entry1.get())
        num2=float(entry2.get())
        operation=operation_label.cget("text")
        if operation=="+":
            result=num1+num2
        elif operation=="-":
            result=num1-num2
        elif operation=="x":
            result=num1*num2
        elif operation=="/":
            result=num1/num2
        else:
            result="Invalid operation"
        result_label.config(text=f"Result:{result}")
    except ValueError:
        result_label.config(text="Please enter valid numeric values")
current_operation = StringVar(value="+")
operation_label = Label(root, textvariable=current_operation, font=("Arial", 12, "bold"), bg="Light blue")
operation_label.grid(row=0, column=2, padx=18, pady=10)
result_label = Label(root, text="", font=("Arial", 12, "bold"), bg="Light yellow")
result_label.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
calculate_button = Button(root, text="Calculate", font=("Arial", 12, "bold"), command=calculate_result)
calculate_button.grid(row=2, column=0, columnspan=5, padx=10, pady=10)
Button(root, text="+", font=("Arial", 12, "bold"), command=lambda: current_operation.set("+")).grid(row=1, column=0, padx=5, pady=5)
Button(root, text="-", font=("Arial", 12, "bold"), command=lambda: current_operation.set("-")).grid(row=1, column=1, padx=5, pady=5)
Button(root, text="*", font=("Arial", 12, "bold"), command=lambda: current_operation.set("*")).grid(row=1, column=2, padx=5, pady=5)
Button(root, text="/", font=("Arial", 12, "bold"), command=lambda: current_operation.set("/")).grid(row=1, column=3, padx=5, pady=5)
root.mainloop()