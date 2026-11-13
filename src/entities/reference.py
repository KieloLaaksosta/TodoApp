class Reference():
    def __init__(self, reference_type, key, author, title, year, publisher):
        # only book references for now
        self.type = reference_type
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher

    def __str__(self):
        return f"{self.key}: {self.title} by {self.author}"

# testi :)
if __name__ == "__main__":
    print(Reference(
        "book", "jdsfjijff3842", "Bill Wat", "The Heidelberg of Bringing", "1405", "Otava"
    ))
