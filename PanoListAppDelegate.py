#
#  PanoListAppDelegate.py
#  PanoList
#
#  Created by Matthieu DESILE on 11/26/2010.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

from Foundation import *
import objc
from AppKit import *

class PanoListAppDelegate(NSObject):


    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

	def applicationWillTerminate_(self,sender):
		NSLog("Application will terminate.")
		
	def applicationSupportFolder(self):
		paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
		basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
		fullPath = basePath.stringByAppendingPathComponent_("Panolist")
		if not os.path.exists(fullPath):
			os.mkdir(fullPath)
		return fullPath
        
	def pathForFilename(self,filename):
		return self.applicationSupportFolder().stringByAppendingPathComponent_(filename)