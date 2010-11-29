#
#  main.py
#  PanoList
#
#  Created by Matthieu DESILE on 11/26/2010.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import PanoListAppDelegate
import PLController

# pass control to AppKit
AppHelper.runEventLoop()
