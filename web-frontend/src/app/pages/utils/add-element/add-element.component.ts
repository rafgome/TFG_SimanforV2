import { Component, Inject, Input, OnInit } from "@angular/core";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material";

@Component({
  selector: "app-add-element",
  templateUrl: "./add-element.component.html",
  styleUrls: ["./add-element.component.scss"],
})
export class AddElementComponent implements OnInit {
  @Input() dataModel: any;
  @Input() dataModelName: string;
  @Input() editId: string;
  @Input() numRequestedUsers: number;
  @Input() numActualUser: number;
  selected: string = "xlsx";
  validInput: boolean = false;
  confirmPassword: string;
  validPassword: boolean = true;
  passwordFieldType: string = 'password';
  confirmPasswordFieldType: string = 'password';

  constructor(
    public dialogRef: MatDialogRef<AddElementComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  fileInputChange(fileInputEvent: any, fieldName: string) {
    this.data[fieldName] = fileInputEvent.target.files[0];
  }

  resetFileInput() {
    this.data["xlsx"] = undefined;
    this.data["csvPlot"] = undefined;
    this.data["csvTree"] = undefined;
    this.validInput = true;
  }

  ngOnInit(): void {
    if (this.editId) {
      this.data.id = this.editId;
    }

    this.dataModel.forEach((field) => {
      if (typeof field.default !== "undefined") {
        this.data[field.name] = field.default;
      }
    });
    this.data['actualUser'] = this.numActualUser;

    if(this.editId && this.dataModelName === 'users') {
      this.validInput = true;
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  updateValidInput() {
    for (const element of this.dataModel) {
      if (
        (element.required &&
        element.name !== "file" &&
        element.name !== "public" &&
        !this.data[element.name]) ||
        !this.validPassword
      ) {
        this.validInput = false;
        return;
      }
    }
    this.validInput = true;
  }

  updateValidPassword(): void {
    if (this.data['password'] !== this.confirmPassword) {
      this.validPassword = false;
    } else {
      this.validPassword = true;
    }
  }

  togglePasswordVisibility() {
    this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
  }

  toggleConfirmPasswordVisibility() {
    this.confirmPasswordFieldType = this.confirmPasswordFieldType === 'password' ? 'text' : 'password';
  }

  refuseUser(): void {
    this.data.status = 'REFUSED';
    this.dialogRef.close(this.data);
  }

  previousUser(): void {
    this.data['actualUser'] = this.data['actualUser'] - 1;
    this.dialogRef.close(this.data);
  }

  nextUser(): void {
    this.data['actualUser'] = this.data['actualUser'] + 1;
    this.dialogRef.close(this.data);
  }
}
