

def save_file(data) -> None:

    with open("data.txt", "w") as f:
        f.writelines(f"{element}\n" for element in data)
        f.close()
    
    print("\nФайл был успешно сохранён!\n")