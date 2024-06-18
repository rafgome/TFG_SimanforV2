import { Component, Input } from "@angular/core";

@Component({
  selector: "app-basic-spinner",
  templateUrl: "./basic-spinner.component.html",
  styleUrls: ["./basic-spinner.component.scss"],
})
export class BasicSpinner {
  @Input() visible: boolean;
}
