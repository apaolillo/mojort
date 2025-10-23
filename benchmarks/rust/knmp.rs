// Rust Program to implement the
// working of KMP Algorithm

use std::{
    env::args,
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

// Function to compute the LPS array
fn compute_lps_array(pattern: &[u8], m: usize, lps: &mut [usize]) {
    let mut length = 0;
    lps[0] = 0; // LPS[0] is always 0
    let mut i = 1;

    while i < m {
        if pattern[i] == pattern[length] {
            length += 1;
            lps[i] = length;
            i += 1;
        } else if length != 0 {
            length = lps[length - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
}

// KMP algorithm to search for
// pattern in text
fn kmp(pattern: &[u8], text: &[u8]) -> Vec<usize> {
    let m = pattern.len();
    let n = text.len();

    // Array for storing the starting index
    // of text, where the pattern exist
    let mut ans = vec![];

    let mut lps = vec![0; m];
    compute_lps_array(pattern, m, &mut lps);

    let mut i = 0; // index for text
    let mut j = 0; // index for pattern
    while i < n {
        // When character matches so we
        // have to increase both the pointers
        if pattern[j] == text[i] {
            i += 1;
            j += 1;
        }

        // When the pattern is completely matched,
        // store the starting position of text,
        // Where the pattern exist
        if j == m {
            ans.push(i - j);
            j = lps[j - 1];
        } else if i < n && pattern[j] != text[i] {
            // When the character is not matched,
            // we have to move to previous index up
            // to which the matches take place
            if j != 0 {
                j = lps[j - 1];
            } else {
                i += 1;
            }
        }
    }

    ans
}

fn main() {
    let bible = File::open("../the_bible.txt").unwrap();
    let mut bible = BufReader::new(bible);

    let mut text = String::new();
    bible.read_line(&mut text).unwrap();
    let p: f64 = args().nth(1).unwrap().parse().unwrap();
    let len = text.len();
    let newlen = (len as f64 * p) as usize;

    let text = &text[0..newlen];
    let pattern = "God";

    let t1 = Instant::now();
    let ans = kmp(pattern.as_bytes(), text.as_bytes());
    let duration = t1.elapsed();

    // printing the index of the last found match
    // done so the compiler wont remove the workload
    println!("checkvalue: {}", ans[ans.len() - 1]);
    println!("runtime: {} µs", duration.as_micros());
}
