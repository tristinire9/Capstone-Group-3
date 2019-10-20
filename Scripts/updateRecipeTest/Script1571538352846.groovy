import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

WebUI.openBrowser('https://intense-stream-78237.herokuapp.com/')

WebUI.click(findTestObject('Page_ITL Component Store/a_Recipes (7)'))

WebUI.click(findTestObject('Page_ITL Component Store/button_1112 (4)'))

WebUI.click(findTestObject('Object Repository/Page_Versions/button_Edit'))

WebUI.setText(findTestObject('Page_ITL Component Store/input_Software NameVersion NumberStatusIn DevelopmentReleased_name'), 
    'softwareRelease16')

WebUI.setText(findTestObject('Page_ITL Component Store/input_Software NameVersion NumberStatusIn DevelopmentReleased_version'), 
    '1.1.19')

WebUI.click(findTestObject('Page_ITL Component Store/input_Software NameVersion NumberStatusIn DevelopmentReleased_status'))

WebUI.click(findTestObject('Page_ITL Component Store/button_Submit (3)'))

WebUI.closeBrowser()

