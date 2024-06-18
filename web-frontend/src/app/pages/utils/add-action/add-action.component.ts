import { Component, Inject, Input, OnInit } from "@angular/core";
import { MAT_DIALOG_DATA, MatDialogRef, MatDialog } from "@angular/material";
import { InventoryService } from "../../../_services/inventory.service";
import { Inventory } from "../../../_models/inventory";
import { TableDialogComponent } from "../table/table.component";

@Component({
  selector: "app-add-action",
  templateUrl: "./add-action.component.html",
  styleUrls: ["./add-action.component.scss"],
})
export class AddActionComponent implements OnInit {
  @Input() dataModel: any;
  @Input() dataModelName: string;
  @Input() editId: string;
  inventories: Inventory[];
  inventory: Inventory;

  constructor(
    public dialogRef: MatDialogRef<AddActionComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    public dialog: MatDialog,
    private inventoryService: InventoryService
  ) {}

  fileInputChange(fileInputEvent: any, fieldName: string) {
    const reader = new FileReader();
    const name: string = fileInputEvent.target.files[0].name;
    reader.onload = () => {
      this.data[fieldName] = JSON.parse(reader.result as string);
      this.data["fileName"] = name;
    };
    reader.readAsText(fileInputEvent.target.files[0]);
  }

  ngOnInit(): void {
    if (this.editId) {
      this.data.id = this.editId;
    }

    this.dataModelName = "inventory_actions";

    this.dataModel.forEach((field) => {
      if (typeof field.default !== "undefined") {
        this.data[field.name] = field.default;
      }
    });

    this.inventoryService.getSmarteloInventories().subscribe(
      (resp) => {
        this.inventories = resp.data;
        this.inventories.forEach((invent) => {
          const creatDate = new Date(invent.creationDate).toLocaleDateString(
            "es-es"
          );
          invent["creationDateHR"] = creatDate;
        });
      },
      (error) => {
        console.error(error);
      }
    );
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  selectInventoryDialog(): void {
    const dialogRef = this.dialog.open(TableDialogComponent, {
      height: "500px",
      width: "900px",
      data: {
        tableTitle: "inventories",
        rowButtons: [],
        tableBody: this.inventories,
        tableHeader: [
          "name",
          "type",
          "creationDateHR",
          "creator",
          "public",
          "fileUrl",
        ],
        selectable: true,
        allowMultiSelect: false,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (!result) {
        return;
      }

      const inventory = result[0];

      if (!inventory) {
        return;
      }

      this.inventory = inventory;
    });
  }

  close(): void {
    this.dialogRef.close({
      inventory: this.inventory,
      data: this.data,
    });
  }
}
