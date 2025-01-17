# Hanja getter
Check code documentation here : https://tiphainejh.github.io/hanja/
# TODO
- [ ] Add functionality to search korean text even if its not full

### 1. **Creation of the database**

- **Data collection**: Korean dictionary obtained from 'https://raw.githubusercontent.com/garfieldnate/kengdic/master/datapackage.json' and hanja obtained from https://github.com/myungcheol/hanja.
- **Data structure **: Two databases created with sqlite3.

### 2. **Development of an association algorithm**

- **Morphological analysis**: Develop a tool that breaks down Korean words into their hanja components. This may involve the use of specialized natural language processing (NLP) libraries for Korean.
- **Word association**: Once the hanja have been identified for a given word, search for all the other words that share these same characters. You can create indexes or relationship tables to make this search easier.

### 3. **User Interface Design**

- **Web or mobile application**: Determine the platform best suited to your needs. A web app would be accessible from any device, while a mobile app could offer a more personalized experience.
- **Key Features**:
  - **Korean word entry**: Allow the user to enter the word they want to study.
  - **Display of corresponding hanja**: Show the hanja characters associated with the entered word.
  - **List of related words**: Display a list of words that contain the same hanja, with their definitions and examples.
  - **Favorites and Notes**: Allow the user to save words and add annotations for easy revision later.

### 4. **Improved user experience**

- **Graphical visualization**: Integrate graphics or mind maps to visually represent the links between words and their Hanja roots.
- **Advanced search**: Add filters to sort words by frequency of use, language level (formal/informal), or field (scientific, literary, etc.).

### 5. **Later improvements**

- **Dictionnary API** : https://opendict.korean.go.kr/service/openApiInfo 

# Brainstorming ideas for name

- 언어의 뿌리 (Eoneoui Ppuri: "Roots of Language").
- 배움의 연결 (Baeum-ui Yeongyeol: "Connections of Learning").
- 한자풀 (Hanja Pul: "Hanja Unraveled").
- 뿌리와 말 (Ppuri wa Mal: "Roots and Words").