#!/usr/bin/perl

undef $/;
while (<>) {
    s/^(\d+)\.\n(.*) (\d\d:\d\d)/${1}|${2}|${3}/gm;
    print;
}
