#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stack>
#include <vector>
#include <Windows.h>
#include <conio.h>

using namespace std;

string trim(string s) {
    s.erase(0, s.find_first_not_of(" \t\r\n"));
    s.erase(s.find_last_not_of(" \t\r\n") + 1);
    return s;
}

void printStack(stack<string> s, string currentName, string currentId) {
    vector<string> items;
    while (!s.empty()) {
        items.push_back(s.top());
        s.pop();
    }

    cout << "\n  Name : " << currentName << endl;
    cout << "  ID   : " << currentId << endl;
    cout << "\n+----------------+" << endl;
    cout << "|   STACK        |" << endl;
    cout << "+----------------+" << endl;
    for (int i = 0; i < (int)items.size(); i++) {
        if (i == 0)
            cout << "|  " << items[i] << " <- top" << endl;
        else
            cout << "|  " << items[i] << endl;
    }
    if (items.empty())
        cout << "|  (empty)       |" << endl;
    cout << "+----------------+" << endl;
    cout << "  size: " << items.size() << endl;
}

void waitKey() {
    cout << "\n[Press any key...]" << endl;
    (void)_getch();
    system("cls");
}

int main() {
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    ifstream file("data.csv");
    if (!file.is_open()) {
        cout << "File not found!" << endl;
        return 1;
    }

    string line;
    getline(file, line); // 헤더 건너뜀

    // 사람별로 저장
    struct Person {
        string name, id, w1, w2, w3;
    };
    vector<Person> people;

    while (getline(file, line)) {
        stringstream ss(line);
        Person p;
        getline(ss, p.name, ',');
        getline(ss, p.id, ',');
        getline(ss, p.w1, ',');
        getline(ss, p.w2, ',');
        getline(ss, p.w3, ',');
        p.name = trim(p.name);
        p.id = trim(p.id);
        p.w1 = trim(p.w1);
        p.w2 = trim(p.w2);
        p.w3 = trim(p.w3);
        people.push_back(p);
    }
    file.close();

    stack<string> stk;

    // 스택 선언 화면
    cout << "=== Stack Animation ===" << endl;
    cout << "Stack declared! (max size: 10)" << endl;
    stack<string> empty;
    printStack(empty, "-", "-");
    waitKey();

    // 사람별 애니메이션
    for (auto& p : people) {

        // push 3개
        vector<string> words = { p.w1, p.w2, p.w3 };
        for (auto& w : words) {
            cout << ">> stack.push(\"" << w << "\")" << endl;
            stk.push(w);
            printStack(stk, p.name, p.id);
            waitKey();
        }

        // top 확인
        cout << ">> stack.top() = \"" << stk.top() << "\"" << endl;
        printStack(stk, p.name, p.id);
        waitKey();

        // pop 3개
        for (int i = 0; i < 3; i++) {
            cout << ">> stack.pop() -> removed: \"" << stk.top() << "\"" << endl;
            stk.pop();
            printStack(stk, p.name, p.id);
            waitKey();
        }
    }

    cout << "=== Done! Stack is empty ===" << endl;
    return 0;
}
