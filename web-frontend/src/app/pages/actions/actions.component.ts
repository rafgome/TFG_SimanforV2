import { Component, OnInit, ElementRef, ViewChild } from "@angular/core";
import { Actions } from "../../_models/actions";
import { MatDialog } from "@angular/material";
import { MatSnackBar } from "@angular/material/snack-bar";
import { TranslateService } from "@ngx-translate/core";
import { TableComponent } from "../utils/table/table.component";
import { ActionService } from "../../_services/actions.service";
import { ShowActionComponent } from "../utils/show-action/show-action.component";

@Component({
  selector: "app-action",
  templateUrl: "./actions.component.html",
  styleUrls: ["./actions.component.css"],
})
export class ActionsComponent implements OnInit {
  actions: Actions[];
  addForm: any[];
  header: string[];
  adBlockerEnabled: boolean;
  @ViewChild("wrapadtest") adElementView: ElementRef;
  bannerVisible: boolean;
  onlyDownload: boolean;
  successfullyBanner: boolean;
  errorBanner: boolean;

  @ViewChild(TableComponent)
  private tableComponent: TableComponent;

  constructor(
    private actionService: ActionService,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.loadTableBody();
    this.addForm = [
      {
        name: "type",
        type: "select",
        values: ["json"],
        default: "json",
        required: true,
      },
      {
        name: "file",
        type: "file",
        accept: [".json"],
        required: true,
      },
    ];

    this.header = [
      "inventoryId",
      "_id",
      "creator",
      "creationDateHR",
      "smarteloFile",
    ];
  }

  resetBanners(): void {
    this.bannerVisible = false;
    this.successfullyBanner = false;
    this.errorBanner = false;
  }

  generateSmartelo(event): void {
    this.resetBanners();
    this.onlyDownload = event.onlyDownload;
    this.bannerVisible = true;
    this.actionService.generateSmartelo(event.id).subscribe(
      (resp) => {
        this.bannerVisible = false;
        this.successfullyBanner = true;
        console.log("ADD OK");
        console.log(resp);
        this.loadTableBody();
        this.downLoadFile(
          resp,
          event.id,
          "application/vnd.ms-excel.sheet.macroenabled.12"
        );
      },
      (error) => {
        console.log("ADD KO", error.status);
        this.bannerVisible = false;
        this.errorBanner = true;
      }
    );
  }

  downLoadFile(data: any, id: number, type: string) {
    let blob = new Blob([data], { type: type });
    let url = window.URL.createObjectURL(blob);
    let file = document.createElement("a");
    file.href = url;
    file.download = `smartelo_${id}`;
    file.click();
  }

  details(dataModel): void {
    const dialogRef = this.dialog.open(ShowActionComponent, {
      data: {},
    });

    if (dataModel) {
      dialogRef.componentInstance.dataModel = dataModel;
    }

    dialogRef.afterClosed().subscribe(() => {
      this.loadTableBody();
    });
  }

  delete(id): void {
    this.actionService.deleteAction(id).subscribe(
      (resp) => {
        console.log("Delete OK");
        this.loadTableBody();
      },
      (error) => {
        console.log("Delete KO");
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  addActions(result?): void {
    if (!result.inventory) {
      this._showSnack(
        "Error: " + this.translate.instant("error.inventory_not_selected")
      );
      return;
    }
    this.actionService
      .addAction({
        ...result.data.file,
        inventory: result.inventory ? result.inventory.inventoryId : "",
      })
      .subscribe(
        (resp) => {
          console.log("ADD OK");
          this.loadTableBody();
        },
        (error) => {
          console.log("ADD KO");
          this._showSnack(
            "Error: " +
              this.translate.instant("error." + error.error.string_code)
          );
        }
      );
  }

  loadTableBody(): void {
    console.log("Loading data...");
    this.actionService.getActions().subscribe(
      (resp) => {
        this.actions = resp.data;
        this.actions.forEach((action) => {
          const date = new Date(action.creationDate).toLocaleDateString(
            "es-es"
          );
          action["creationDateHR"] = date;
        });
      },
      (error) => {
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  _showSnack(message: string, duration = 6000): void {
    this.snackBar.open(message, "Close", {
      duration: duration,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }

  closeBanner1(): void {
    this.bannerVisible = false;
  }

  closeBanner2(): void {
    this.successfullyBanner = false;
  }

  closeBanner3(): void {
    this.errorBanner = false;
  }
}
