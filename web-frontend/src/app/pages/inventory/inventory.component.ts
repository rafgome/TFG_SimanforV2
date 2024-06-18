import { Component, OnInit } from "@angular/core";
import { Inventory } from "../../_models/inventory";
import { InventoryService } from "../../_services/inventory.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { TranslateService } from "@ngx-translate/core";

@Component({
  selector: "app-inventory",
  templateUrl: "./inventory.component.html",
  styleUrls: ["./inventory.component.css"],
})
export class InventoryComponent implements OnInit {
  inventories: Inventory[];
  header: string[];
  addForm: any[];

  constructor(
    private inventoryService: InventoryService,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.loadTableBody();
    this.addForm = [
      {
        name: "name",
        type: "string",
        required: true,
      },
      {
        name: "year",
        type: "number",
        required: true,
      },
      {
        name: "_id",
        type: "show",
        required: false,
        editable: false,
      },
      {
        name: "creator",
        type: "show",
        required: false,
        editable: false,
      },
      {
        name: "fileUrl",
        type: "show",
        required: false,
        editable: false,
      },
      {
        name: "type",
        type: "select",
        values: ["xlsx", "csv"],
        default: "xlsx",
        required: true,
        editable: false,
      },
      {
        name: "public",
        type: "boolean",
        default: false,
        required: true,
      },
      {
        name: "smartelo",
        type: "chip",
        required: true,
      },
      {
        name: "file",
        type: "file",
        required: true,
      },
    ];
    this.header = [
      "name",
      "creationDateHR",
      "creator",
      "public",
      "smartelo",
    ];
  }

  add(data): void {
    this.inventoryService.addInventory(data).subscribe(
      (resp) => {
        console.log("ADD OK");
        console.log(resp);
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

  edit(data: Inventory): void {
    this.inventoryService.editInventory(data).subscribe(
      (resp) => {
        console.log("Edit OK");
        this.loadTableBody();
      },
      (error) => {
        console.log("Edit KO", error);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  delete(id): void {
    this.inventoryService.deleteInventory(id).subscribe(
      (resp) => {
        console.log("Delete OK");
        this.loadTableBody();
      },
      (error) => {
        console.log("Delete KO", error);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  loadTableBody(): void {
    console.log("Loading data...");
    this.inventoryService.getInventories().subscribe(
      (resp) => {
        this.inventories = resp.data;
        this.inventories.forEach((invent) => {
          const creatDate = new Date(invent.creationDate).toLocaleDateString(
            "es-es"
          );
          invent["creationDateHR"] = creatDate;
          invent["smartelo"] = invent["smartelo"] ? "Smartelo" : "Simanfor";
        });
      },
      (error) => {
        console.log(error.status);
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
