//
//  ViewController.swift
//  Quiz
//
//  Created by 渕上豪支 on 2021/02/11.
//

import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var startButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        startButton.layer.borderWidth=2
        startButton.layer.borderColor=UIColor.black.cgColor
    }


}

