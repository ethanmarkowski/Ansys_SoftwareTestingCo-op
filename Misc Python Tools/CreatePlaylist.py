import os
import re
import sys

def list_of_testnames(cs_file):
    # Function iterates through the TestSuites and returns a dictionary of the tests
    list_of_tests = []  # contains list of tests in each Suite
    for line in cs_file:
        if (line.find('public async') != -1):
            test_name = re.findall("Task (.*?)\(\)", line)
            list_of_tests.append(test_name[0])
    return list_of_tests

def create_playlist(disco_repo_filepath = '', test_list_filepath = '', playlist_name = ''):
    # Inputs for local Disco repository and list of tests to create a playlist from
    if disco_repo_filepath == '':
        disco_repo_filepath = input("Input local Disco repository path:\n")
    if os.path.isdir(disco_repo_filepath) == False:
        print ("Directory does not exist: " + disco_repo_filepath)
        sys.exit()
    if test_list_filepath == '':
        test_list_filepath = input("Enter a text file that contains list of tests:\n")
    if os.path.isfile(test_list_filepath) == False:
        print ("File does not exist: " + test_list_filepath)
        sys.exit()
    if playlist_name == '':
        playlist_name = input("Name of your playlist?: ")

    # Generate list of TestSuite file paths
    list_of_paths = []
    for (root, dirs, files) in os.walk(disco_repo_filepath):
        for next_file in files:
            if next_file.endswith(".cs") and ("JournalTests" in root):
                cs_path = root + "\\" + next_file
                list_of_paths.append(cs_path)

    # Create a dictionary of (Testsuites: [tests])
    test_inventory = {}
    for cs_file in list_of_paths: # opens each filepath
        with open(cs_file) as next_cs_file:
            dict_key = os.path.basename(cs_file)
            test_list = list_of_testnames(next_cs_file) # returns test_inventory dictionary
            test_inventory[dict_key] = test_list

    # Open the given list of tests and find what TestSuite they are in
    # Generate playlist based off TestSuite name and TestName
    with open(test_list_filepath, 'r+') as test_list :
        # get root dir of test_list_filepath
        playlist_dir = test_list_filepath.strip(os.path.basename(test_list_filepath)) 
        with open(playlist_dir + playlist_name + '.playlist', 'w+') as playlist: 
            # creating new playlist file
            playlist.write('<Playlist Version=\"1.0\">') 
            for next_test in test_list:
                next_test = next_test.rstrip()
                for next_key in test_inventory:
                    for test in test_inventory[next_key]:
                        # check if test is in the testsuite
                        if test == next_test:
                            # add test to playlist
                            playlist.write("<Add Test=\"Ansys.Disco.Integration.Tests.JournalTests." + next_key.strip(".cs") + "." + next_test + '\" />')
            playlist.write('</Playlist>')

DiscoRepoFolderpath = "C:\\Users\\cjconnel\\source\\repos\\Disco"
TestListFilepath = "C:\\Shared\\BeingHelpful\\Jitesh\\ScdocTestList2.txt"
PlaylistFilename = "ScdocTestList"
create_playlist(DiscoRepoFolderpath, TestListFilepath, PlaylistFilename)