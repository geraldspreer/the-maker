#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
from makerUpdateSandboxedProjects import UpdateSandboxedProjects as theUpdater
import makerUpdateSandboxedProjects
import sys
from makerUtilities import writeDataToFile, readDataFromFile
import wx


class MakerTest(unittest.TestCase):
    def tearMeDown(self):

        if os.path.isdir(self.targetDir):
            shutil.rmtree(self.targetDir, ignore_errors=True)

    def setMeUp(self):

        self.user_home = "/Users/maker/"

        testProjects = os.path.join(os.getcwd(), "_Testing_")
        self.tool = theUpdater()

        self.targetDir = self.tool.getConversionTargetDir()

        self.sandbox = self.tool.getApplicationSupportDir()

        self.oldProjectsDir = os.path.join(self.sandbox, "makerProjects")

        self.UIData = {
            "SplitterSashPosition": 200,
            "editorStyle": "Github",
            "sessionFiles": [
                [u"index_en", ".content", u"Test.makerProject", 0, "False"],
                [u"bootstrap-alert", ".js", u"Test.makerProject", 0, "False"],
                [u"bootstrap-collapse", ".js", u"Test.makerProject", 97, "True"],
            ],
            "linkedProjects": [u"/Users/maker/Desktop/Test.makerProject"],
            "Position": wx.Point(120, 36),
            "Size": wx.Size(1200, 796),
        }

        if os.path.isdir(self.sandbox):
            shutil.rmtree(self.sandbox, ignore_errors=True)

        shutil.copytree(testProjects, self.oldProjectsDir)
        writeDataToFile(self.UIData, os.path.join(self.sandbox, ".makerUISettings"))

    def test_getCorrectTargetDir(self):
        self.setMeUp()

        self.assertTrue(
            self.targetDir.endswith(makerUpdateSandboxedProjects.TARGET_NAME),
            "Target dir set correct",
        )

        self.tearMeDown()

    def test_ifNoMakerProjectsDirInSandboxDoNothing(self):
        self.setMeUp()

        if os.path.isdir(self.oldProjectsDir):
            shutil.rmtree(self.oldProjectsDir)

        self.tool.update()

        self.assertFalse(os.path.isdir(self.targetDir), "There should be no target dir")

        self.tearMeDown()

    def test_ifNoProjectsInSandboxDoNothing(self):

        self.setMeUp()

        if os.path.isdir(self.oldProjectsDir):
            shutil.rmtree(self.oldProjectsDir)

        print "creating empty projects dir"

        os.mkdir(os.path.join(self.sandbox, "makerProjects"))
        self.assertTrue(
            os.path.isdir(os.path.join(self.sandbox, "makerProjects")),
            "Project dir is there...",
        )
        self.assertEqual(os.listdir(self.oldProjectsDir), [], "It is empty...")

        self.tool.update()

        self.assertFalse(os.path.isdir(self.targetDir), "There should be no target dir")

        self.tearMeDown()

    def test_existingProjectsWillBeConverted(self):
        def isProject(project):
            if os.path.isdir(os.path.join(project, "parts")):
                return True
            else:
                return False

        def getProjectsInSandbox():
            projects = []
            for item in os.listdir(self.oldProjectsDir):
                if not item.startswith(".") and isProject(
                    os.path.join(self.oldProjectsDir, item)
                ):
                    projects.append(item)

            return projects

        self.setMeUp()

        self.assertNotEqual(os.listdir(self.oldProjectsDir), [], "It is empty...")

        print "creating JUNK project..."
        junk = "IamNotAProject"
        spam = os.path.join(self.oldProjectsDir, junk)
        os.mkdir(spam)

        self.assertTrue(os.path.isdir(spam), "Junk project is there...")

        oldProjects = getProjectsInSandbox()

        self.assertTrue("TestProjectOne" in oldProjects, "Old project in list")

        self.tool.update()

        self.assertTrue(os.path.isdir(self.targetDir), "There should be no target dir")
        self.assertFalse(
            os.path.isdir(self.oldProjectsDir), "There should be no old project dir"
        )

        fileInTarget = os.listdir(self.targetDir)

        for item in oldProjects:
            self.assertTrue(
                item + ".makerProject" in fileInTarget,
                "project has been converted and copied",
            )

        self.assertFalse(
            junk + ".makerProject" in fileInTarget,
            "JUNK project has NOT been converted and copied",
        )

        self.tearMeDown()


if __name__ == "__main__":
    unittest.main()
