#pragma once
#include <fstream>
#include <string>
#include <vector>

class Logger {
public:
    Logger();             // ctor
    ~Logger();            // dtor: ensure file closed
    void openNewFile();   // create timestamped CSV in logs/
    void bufferRow(const std::vector<std::string>& row);
    void flush();         // flush any buffered rows
    void close();         // close file

private:
    std::ofstream ofs;
    std::vector<std::vector<std::string>> buffer;
};