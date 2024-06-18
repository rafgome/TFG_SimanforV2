import { Component, OnInit } from "@angular/core";
import { User } from "../../_models/user";
import { UsersService } from "./../../_services/users.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { TranslateService } from "@ngx-translate/core";
import { AuthService } from "../../_services/auth.service";
import { Router } from "@angular/router";

@Component({
  selector: "app-users",
  templateUrl: "./users.component.html",
  styleUrls: ["./users.component.css"],
})
export class UsersComponent implements OnInit {
  header: string[];
  users: User[];
  addForm: any[];
  requestedUsers: User[];
  numRequestedUsers: number;

  constructor(
    private usersService: UsersService,
    private snackBar: MatSnackBar,
    private translate: TranslateService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (
      !this.authService.isAuthenticated() ||
      this.authService.getRole() !== "admin"
    ) {
      this.router.navigate(["/"]);
    }

    this.addForm = [
      {
        name: "user",
        type: "show",
        required: true,
      },
      {
        name: "name",
        type: "show",
        required: true,
      },
      {
        name: "surname",
        type: "show",
        required: true,
      },
      {
        name: "status",
        type: "status",
        required: true,
      },
      {
        name: "center",
        type: "show",
        required: true,
      },
      {
        name: "department",
        type: "show",
        required: true,
      },
      {
        name: "email",
        type: "show",
        required: true,
      },
      {
        name: "phone",
        type: "show",
        required: true,
      },
      {
        name: "role",
        type: "show",
        required: true,
      },
    ];

    this.header = [
      "user",
      "name",
      "surname",
      "center",
      "department",
      "email",
      "phone",
      "role",
    ];
    this.loadTableBody();
    this.getRequestedUsers();
  }

  add(data): void {
    this.usersService.updateUser(data).subscribe(
      (resp) => {
        console.log("ADD OK");
        console.log(resp);
        this.loadTableBody();
        this.getRequestedUsers();
      },
      (error) => {
        console.log("ADD KO", error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  delete(id): void {
    this.usersService.deleteUser(id).subscribe(
      (resp) => {
        console.log("Delete OK");
        this.loadTableBody();
        this.getRequestedUsers();
      },
      (error) => {
        console.log("Delete KO", error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  loadTableBody(): void {
    this.usersService.getUsers().subscribe(
      (resp) => {
        this.users = resp.data;
      },
      (error) => {
        console.error(error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
    
  }

  getRequestedUsers(): void{
    this.usersService.getRequestedUsers().subscribe(
      (resp) => {
        this.requestedUsers = resp.data;
        this.numRequestedUsers = this.requestedUsers.length;
      },
      (error) => {
        console.error(error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  _showSnack(message: string): void {
    this.snackBar.open(message, "Close", {
      duration: 6000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}
