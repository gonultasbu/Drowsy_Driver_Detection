#include <iostream>
#include <fstream>

using namespace std;

void gen_file(ifstream& input_file_param, ofstream& output_file_param){
    string start="0",stop="0";
    int c;
    getline(input_file_param,start);
    while(getline(input_file_param,start,' ')){

        for(c=stoi(stop);c<=stoi(start);c++){ //generate the zeros
            output_file_param<<"0";
        }

        getline(input_file_param,stop);
        //stop.pop_back(); //Get rid of the newline character, remove on DOS while compiling

        for(c=stoi(start);c<=stoi(stop);c++){ //generate the ones
            output_file_param<<"1";
        }
    }
}


int main() {
    ifstream input_file;
    input_file.open("sleepyCombination.txt");
    ofstream output_file;
    output_file.open("generatedFile.txt");

    gen_file(input_file,output_file);

    output_file.close();
    input_file.close();
    return 0;
}