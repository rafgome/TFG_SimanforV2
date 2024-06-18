import { Component, Inject } from "@angular/core";
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from "@angular/material";
import { Model } from "../../_models/model";
import { ModelService } from "../../_services/model.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { TranslateService } from "@ngx-translate/core";
import { AuthService } from "../../_services/auth.service";
import { Router } from "@angular/router";

@Component({
  selector: "app-dialog-overview-example-dialog",
  template: `<h1 mat-dialog-title>Hi {{ data.name }}</h1>
    <div mat-dialog-content>
      <p>What's your favorite animal?</p>
      <mat-form-field>
        <input matInput tabindex="1" [(ngModel)]="data.animal" />
      </mat-form-field>
    </div>
    <div mat-dialog-actions>
      <button mat-button [mat-dialog-close]="data.animal" tabindex="2">
        Ok
      </button>
      <button mat-button (click)="onNoClick()" tabindex="-1">No Thanks</button>
    </div>`,
})
export class DialogOverviewExampleDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: "app-models",
  templateUrl: "./models.component.html",
  styleUrls: ["./models.component.scss"],
})
export class ModelsComponent {
  models: Model[];
  header: string[];
  addForm: any[];

  constructor(
    public dialog: MatDialog,
    private modelService: ModelService,
    private snackBar: MatSnackBar,
    private translate: TranslateService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(["/"]);
    }

    this.loadTableBody();

    this.addForm = [
      {
        name: "_id",
        type: "show",
        required: false,
        editable: false,
      },
      {
        name: "name",
        type: "string",
        required: true,
      },
      {
        name: "description",
        type: "string",
        required: true,
      },
      {
        name: "type",
        type: "select",
        values: ["cutting", "projection"],
        default: "cutting",
        required: true,
      },
      {
        name: "docs",
        type: "string",
        required: false,
      },
      {
        name: "status",
        type: "select",
        values: ["stable", "indevelopment"],
        default: "stable",
        required: true,
        editable: true,
      },
      {
        name: "modelPath",
        type: "string",
        required: true,
      },

      {
        name: "modelClass",
        type: "string",
        required: true,
      },

      {
        name: "operation",
        type: "string",
        required: true,
      },
      {
        name: "specie",
        type: "string",
        required: false,
      },
      {
        name: "applicationArea",
        type: "string",
        required: false,
      },
      {
        name: "executionPeriod",
        type: "string",
        required: false,
      },
      {
        name: "operatingDimensions",
        type: "string",
        required: false,
      },
    ];
    
    this.header = [
      "name",
      "type",
      "modelClass",
      // "docs",
      "specie",
      "applicationArea",
      "executionPeriod",
      "operatingDimensions",
      "status",
    ];
  }

  add(data): void {
    this.modelService.addModel(data).subscribe(
      (resp) => {
        this.loadTableBody();
      },
      (error) => {
        console.log("ADD KO", error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  edit(data: Model): void {
    this.modelService.editModel(data).subscribe(
      (resp) => {
        console.log("Edit OK");
        this.loadTableBody();
      },
      (error) => {
        console.log("Edit KO", error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  delete(id): void {
    this.modelService.deleteModel(id).subscribe(
      (resp) => {
        console.log("Delete OK");
        this.loadTableBody();
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
    console.log("Loading data...");

    if (this.authService.getRole() === "admin") {
      this.modelService.getModels().subscribe(
        (resp) => {
          this.models = resp.data;
        },
        (error) => {
          console.error(error.status);
          this._showSnack(
            "Error: " +
              this.translate.instant("error." + error.error.string_code)
          );
        }
      );
    } else {
      this.modelService.getProjectionModels().subscribe(
        (resp) => {
          this.models = resp.data;
        },
        (error) => {
          console.error(error.status);
          this._showSnack(
            "Error: " +
              this.translate.instant("error." + error.error.string_code)
          );
        }
      );
    }
  }

  _showSnack(message: string): void {
    this.snackBar.open(message, "Close", {
      duration: 6000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}
