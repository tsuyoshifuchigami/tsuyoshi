//
//  ViewController.swift
//  BMI
//
//  Created by 渕上豪支 on 2021/02/11.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var height: UITextField!
    
    @IBOutlet weak var weight: UITextField!
    
    @IBOutlet weak var bmiText: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.height.keyboardType=UIKeyboardType.numberPad
        self.weight.keyboardType=UIKeyboardType.numberPad
    }
    
    @IBAction func button(_ sender: Any) {
        let dheight=Double(height.text!)
        let dweight=Double(weight.text!)
        let dheight2=(dheight!/100) * (dheight!/100)
        let bmi=String(dweight!/dheight2)
        
        bmiText.text=("あなたのBMIは"+bmi+"です！")
    }
    
}

