#include "12.h"

#include <fstream> // inFile
#include <iostream> // cout
#include <vector>
#include <sstream> // tokenStream


using namespace std;

PlantPopulation::PlantPopulation(string initialState)
: m_initialState(initialState)
, m_state()
, m_formulas()
{
    m_state = stringtobits<uint64_t>(m_initialState, true /*center*/);
}

void PlantPopulation::appendFormula(const string& pattern, const string& result)
{
    m_formulas[stringtobits<uint8_t>(pattern)] = stringtobits<uint8_t>(result) << 2;
}

uint64_t PlantPopulation::evolve()
{ 
    PlantPopulation::Formula bitset(0);

    //cout << "string: " << endl << bitstostring(m_state) << endl;

    uint64_t stateCopy = m_state;
    uint64_t nextGen = 0;
    for (int i = 0; i < 64; i++)
    {
        //cout << stateCopy << endl;
        bitset = (Formula)(stateCopy & ~224);
        stateCopy = stateCopy >> 1;
        //cout << (int)bitset << endl;
        //bitstostring(bitset, 5);
    
        map<Formula,Formula>::iterator it = m_formulas.find(bitset); 
        if (it != m_formulas.end())
        {   
            uint64_t b = m_formulas[bitset];
            //cout << "Formula found! " << bitstostring(bitset) << " with result " << bitstostring(b) << endl;
            nextGen = nextGen | b << i;
            //cout << bitstostring(nextGen) << endl;
        }
    }
    

    m_state = nextGen;
    return nextGen;
}

void PlantPopulation::printPopulation()
{
    cout << bitstostring(m_state) << endl;
}


template <class T>
T PlantPopulation::stringtobits(const string& input, bool center)
{
    T output(0);

    for (const char& c : input) 
    {
        output = output << 1 | ((c == '#') ? 1 : 0); // | b;
    }
    if (center)
    {
        output = output << ((sizeof(T)*8)-input.length())/2;
    }
    //cout << (std::bitset<sizeof(T)*8>)output << endl;
    return output;
}

template <class T>
string PlantPopulation::bitstostring(const T& input, int printSize)
{
    //cout << "Size of: " << sizeof(input) << endl;
    string output;
    for (int i = sizeof(input)*8 - 1; i >= 0; i--)
    {
        bool flower = ((uint8_t)(input >> i) & ~254);
        if (i < printSize)
        {
            cout << ((flower) ? '#' : '.');
        }
        output += (flower) ? '#' : '.';
    }
    if (printSize != 0)
    {
        cout << endl;
    }
    return output;
}

vector<string> split(const string& s, char delimiter)
{
    std::vector<std::string> tokens;
    string token;
    istringstream tokenStream(s);
    
    while (getline(tokenStream, token, delimiter))
    {
        tokens.push_back(token);
    }

    return tokens;
}

PlantPopulation parse(string filename)
{
    const int MAXLINE=256;
    ifstream inFile(filename);
    char oneline[MAXLINE];

    // 1. Initial state:
    inFile.getline(oneline, MAXLINE);
    vector<string> tokens = split(oneline, ' ');
    PlantPopulation pp(tokens[2]);

    // 2. empty line
    inFile.getline(oneline, MAXLINE);

    while (inFile)
    {
        inFile.getline(oneline, MAXLINE);
        tokens = split(oneline, ' ');
        //cout << tokens[0] << "=>" << tokens[2] << endl;;
        pp.appendFormula(tokens[0], tokens[2]);
    }
    return pp;
}


int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        cout << "missing input file" << endl;
        return 1;
    }
    string inputfile = argv[1];
    cout << "Day 12" << endl;

    PlantPopulation pp = parse(inputfile);

    pp.printPopulation();
    for (int i = 0; i < 325; i++)
    {
        pp.evolve();
        pp.printPopulation();
    }
    
    

    return 0;
}