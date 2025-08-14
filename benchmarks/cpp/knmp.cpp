// C++ Program to implement the
// working of KMP Algorithm
#include <iostream>
#include <fstream>
#include <bits/stdc++.h>
using namespace std;

// Function to compute the LPS array
void computeLPSArray(string pattern,
              int m, vector<int> &LPS) {
    int length = 0;
    LPS[0] = 0; // LPS[0] is always 0
    int i = 1;

    while (i < m) {
        if (pattern[i] ==
            pattern[length]) {
            length++;
            LPS[i] = length;
            i++;
        }
        else {
            if (length != 0) {
                length = LPS[length - 1];
            }
            else {
                LPS[i] = 0;
                i++;
            }
        }
    }
}

// KMP algorithm to search for
// pattern in text
vector<int> KMP(string pattern,
                string text) {
    int m = pattern.length();
    int n = text.length();

    // Array for storing the starting index
    // of text, where the pattern exist
    vector<int> ans;

    vector<int> LPS(m);
    computeLPSArray(pattern, m, LPS);

    int i = 0; // index for text
    int j = 0; // index for pattern
    while (i < n) {

        // When character matches so we
        // have to increase both the pointers
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        // When the pattern is completely matched,
        // store the starting position of text,
        // Where the pattern exist
        if (j == m) {
            ans.push_back(i - j);
            j = LPS[j - 1];
        }
        // When the character is not matched,
        // we have to move to previous index up
        // to which the matches take place
        else if (i < n && pattern[j]
                 != text[i]) {
            if (j != 0) {
                j = LPS[j - 1];
            }
            else {
                i++;
            }
        }
    }
    return ans;
}

int main(int argc, char *argv[]) {
    ifstream MyReadFile("../the_bible.txt");
    string text;
    getline(MyReadFile, text);
    double p = atof(argv[1]);
    int len =text.length();
    int newlen = len * p;

    text = text.substr (0,newlen);
    string pattern = "God";

    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    auto t1 = high_resolution_clock::now();
    vector<int> ans = KMP(pattern, text);
    auto t2 = high_resolution_clock::now();

    /* Getting number of milliseconds as a double. */
    duration<double, std::milli> ms_double = t2 - t1;
    // printing a otherwise the compiler will optimize the loop away
    std::cout << int(ans[ans.size()-1]) << "\n";
    std::cout << "runtime: " << int((ms_double.count() * 1000)) << " µs\n";
    return 0;

    cout << "Pattern Found at Indexes: ";
    for (auto i : ans)
        cout << i << " ";
    return 0;
}
