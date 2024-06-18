import { Component, Inject, Input, OnInit, ViewChild } from "@angular/core";
import { MatSort } from "@angular/material/sort";
import { MatPaginator } from "@angular/material/paginator";
import {
  MAT_DIALOG_DATA,
  MatDialogRef,
  MatDialog,
  MatTableDataSource,
} from "@angular/material";
import { Inventory } from "../../../_models/inventory";

@Component({
  selector: "app-show-action",
  templateUrl: "./show-action.component.html",
  styleUrls: ["./show-action.component.scss"],
})
export class ShowActionComponent implements OnInit {
  displayedColumns: string[] = [
    "plot_id",
    "tree_id",
    "species",
    "action",
    "reason",
  ];
  @Input() dataModel?: any;
  dataSource: any;
  inventories: Inventory[];
  inventory: Inventory;
  @ViewChild(MatSort, { static: true }) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  constructor(
    public dialogRef: MatDialogRef<ShowActionComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource(this.dataModel.actions);
    this.dataSource.sort = this.sort;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  close(): void {
    this.dialogRef.close({
      inventory: this.inventory,
      data: this.data,
    });
  }
}
