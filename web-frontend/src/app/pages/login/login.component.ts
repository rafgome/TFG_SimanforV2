import { Component, OnInit } from "@angular/core";
import { ApiService } from "./../../_services/api.service";
import { CommonService } from "./../../_services/common.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { Router } from "@angular/router";
import { AuthService } from "../../_services/auth.service";
import { TranslateService } from "@ngx-translate/core";
import { MatDialog } from "@angular/material";
import { AddElementComponent } from "../utils/add-element/add-element.component";
import { ConfirmationComponent } from "../utils/confirmation/confirmation.component";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.scss"],
})
export class LoginComponent implements OnInit {
  addForm: any[];
  username: string;
  password: string;

  constructor(
    private apiService: ApiService,
    private commonService: CommonService,
    private authService: AuthService,
    private snackBar: MatSnackBar,
    private router: Router,
    private translate: TranslateService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(["inventory"]);
    }
    this.addForm = [
      {
        name: "user",
        type: "string",
        required: true,
      },
      {
        name: "password",
        type: "password",
        required: true,
      },
      {
        name: "password2",
        type: "confirmPassword",
        required: false,
      },
      {
        name: "name",
        type: "string",
        required: true,
      },
      {
        name: "surname",
        type: "string",
        required: true,
      },
      {
        name: "center",
        type: "string",
        required: true,
      },
      {
        name: "department",
        type: "string",
        required: true,
      },
  
      {
        name: "email",
        type: "string",
        required: true,
      },
  
      {
        name: "phone",
        type: "string",
        required: true,
      },
      {
        name: "role",
        type: "select",
        values: ["basic", "admin"],
        default: "basic",
        required: true,
        editable: true,
      },
    ];
  }

  onSubmit(): void {
    const formData = new FormData();
    formData.append("user", this.username);
    formData.append("password", this.password);

    this.apiService.postFormData("/login", formData).subscribe(
      (resp) => {
        this.authService.setAuthToken(resp.data.token);
        this.authService.setRole(resp.data.role);
        this.router.navigate(["inventory"]);
      },
      (error) => {
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  newUserRequest(): void {
    const dialogRef = this.dialog.open(AddElementComponent, {
      data: {},
    });

    dialogRef.componentInstance.dataModelName = 'users';

    let form = [...this.addForm];

    dialogRef.componentInstance.dataModel = form;

    dialogRef.afterClosed().subscribe((result) => {
      // The dialog was closed
      if (result) {
        const confirmation = this.dialog.open(ConfirmationComponent);
        confirmation.componentInstance.message = "table.confirmation_regist_user";
        confirmation.afterClosed().subscribe((res) => {
          if (res) {
            this.apiService.postFormData("/register", this.commonService.objectToFormData(result)).subscribe(
              (resp) => {
                console.log("ADD OK");
                console.log(resp);
              },
              (error) => {
                console.log("ADD KO", error.status);
                this._showSnack(
                  "Error: " + this.translate.instant("error." + error.error.string_code)
                );
              }
            );
          }
        })
      }
    });
  }

  _showSnack(message: string): void {
    this.snackBar.open(message, "Close", {
      duration: 6000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}
