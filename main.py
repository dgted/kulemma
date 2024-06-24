from library.bn_pos_lemmatizer import PosLemmatizer

document = """সরকারি চিকিৎসকদের অনীহার ফলে গ্রামের মানুষ অবিচারের শিকার হচ্ছে বলে মন্তব্য করেছেন পরিকল্পনামন্ত্রী এমএ মান্নান। চিকিৎসকদের গ্রামে গিয়ে সেবা দিতে অনীহার বিষয় উল্লেখ করে মন্ত্রী হতাশা প্রকাশ করেছেন
"""

plemmatizer = PosLemmatizer()
result = plemmatizer.lemmatize(document)
print("lemmatizer", result)
