import {
  Component,
  Inject,
  OnInit,
  Input,
  Output,
  EventEmitter,
} from "@angular/core";
import { CommonService } from "./../../../_services/common.service";
import { TranslateService } from "@ngx-translate/core";
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from "@angular/material";
import { AddElementComponent } from "../add-element/add-element.component";
import { AddActionComponent } from "../add-action/add-action.component";
import { SelectionModel } from "@angular/cdk/collections";
import { ConfirmationComponent } from "../confirmation/confirmation.component";

@Component({
  selector: "app-sim-table-dialog",
  template: ` <app-sim-table
    [tableHeader]="tableHeader"
    [tableBody]="tableBody"
    [tableTitle]="tableTitle"
    [rowButtons]="[]"
    [selectable]="selectable"
    [allowMultiSelect]="allowMultiSelect"
    (onSelectSubmit)="close($event)"
  ></app-sim-table>`,
})
export class TableDialogComponent implements OnInit {
  @Input() tableBody: any[];
  @Input() tableHeader: string[];
  @Input() tableTitle: string;
  @Input() rowButtons?: string[];
  @Input() selectable?: boolean;
  @Input() allowMultiSelect?: boolean;

  constructor(
    public dialogRef: MatDialogRef<ConfirmationComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit(): void {
    this.tableBody = this.data.tableBody;
    this.tableHeader = this.data.tableHeader;
    this.tableTitle = this.data.tableTitle;
    this.rowButtons = this.data.rowButtons;
    this.selectable = this.data.selectable;
    this.allowMultiSelect = this.data.allowMultiSelect;
  }

  public close(result: any): void {
    this.dialogRef.close(result);
  }
}

@Component({
  selector: "app-sim-table",
  templateUrl: "./table.component.html",
  styleUrls: ["./table.component.scss"],
})
export class TableComponent implements OnInit {
  @Input() tableBody: any[];
  @Input() tableHeader: string[];
  @Input() tableTitle: string;
  @Input() rowButtons: string[];
  @Input() addForm: any;
  @Input() requestedUsers: any[];
  @Input() numRequestedUsers: number;
  @Input() selectable?: boolean;
  @Output()
  deleteEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output()
  resultsEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output()
  detailsEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output()
  editEvent: EventEmitter<any> = new EventEmitter<any>();
  @Output()
  addEvent: EventEmitter<any> = new EventEmitter<any>();
  @Input() allowMultiSelect?: boolean;
  @Output() onSelectSubmit: EventEmitter<any> = new EventEmitter();

  // @ts-ignore
  dtOptions: DataTables.Settings = {};

  initialSelection = [];
  selection: SelectionModel<any>;
  loading: boolean;
  numActualUser: number = 0;

  constructor(
    private commonService: CommonService,
    private translate: TranslateService,
    public dialog: MatDialog
  ) {}

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.tableBody.length;
    // tslint:disable-next-line:triple-equals
    return numSelected == numRows;
  }

  masterToggle() {
    this.isAllSelected()
      ? this.selection.clear()
      : this.tableBody.forEach((row) => this.selection.select(row));
  }

  ngOnInit(): void {
    if (this.selectable === undefined) {
      this.selectable = false;
    }
    if (this.allowMultiSelect === undefined) {
      this.allowMultiSelect = true;
    }

    this.selection = new SelectionModel<any>(
      this.allowMultiSelect,
      this.initialSelection
    );
    this.setDataTableOptions();
  }

  setDataTableOptions() {
    this.dtOptions = {
      pagingType: "full_numbers",
      pageLength: 10,
      lengthMenu: [
        [10, 20, -1],
        [10, 20, 'All']
      ],
      processing: true,
      language: this.commonService.getDatatableLanguageConfig(this.translate),
    };
  }

  generateArray(obj) {
    const headers = [...this.tableHeader];

    const result = headers.map((prop) => {
      return obj[prop];
    });

    return result;
  }

  isBoolean(variable) {
    if (typeof variable === "boolean") {
      return true;
    } else {
      return false;
    }
  }

  openDialog(dataValues?): void {
    const dialogRef = this.dialog.open(AddElementComponent, {
      data: {},
    });

    dialogRef.componentInstance.dataModelName = this.tableTitle;

    let form = [...this.addForm];

    if (dataValues) {
      dialogRef.componentInstance.editId = dataValues._id;

      form = form.map((formItem) => {
        if (dataValues[formItem.name]) {
          return (formItem = {
            ...formItem,
            default: dataValues[formItem.name],
          });
        }

        return formItem;
      });
    }

    dialogRef.componentInstance.dataModel = form;

    dialogRef.afterClosed().subscribe((result) => {
      // The dialog was closed
      if (result) {
        console.log("addEvent launched");
        if (!dataValues) {
          this.addEvent.emit(result);
        } else {
          this.editEvent.emit(result);
        }
      }
    });
  }

  openRequestedUsersDialog():void {
    if (this.numRequestedUsers > 0) {
      const dialogRef = this.dialog.open(AddElementComponent, {
        data: {},
      });
  
      dialogRef.componentInstance.dataModelName = this.tableTitle;
  
      let form = [...this.addForm];

      const actualUser = this.requestedUsers[this.numActualUser];
      
      dialogRef.componentInstance.editId = actualUser._id;
      dialogRef.componentInstance.numRequestedUsers = this.numRequestedUsers;
      dialogRef.componentInstance.numActualUser = this.numActualUser;
      
      form = form.map((formItem) => {
        if (actualUser[formItem.name]) {
          return (formItem = {
            ...formItem,
            default: actualUser[formItem.name],
          });
        }

        return formItem;
      });
  
      dialogRef.componentInstance.dataModel = form;
  
      dialogRef.afterClosed().subscribe((result) => {
        // The dialog was closed
        if (result) {
          if (result.actualUser == this.numActualUser){
            const confirmation = this.dialog.open(ConfirmationComponent);
            if(result.status === 'REFUSED') {
              confirmation.componentInstance.message = "table.confirmation_refuse_user";
            } else {
              confirmation.componentInstance.message = "table.confirmation_accept_user";
            }
            confirmation.afterClosed().subscribe((res) => {
              if (res) {
                this.numRequestedUsers--;
                console.log("editEvent launched");
                this.addEvent.emit(result);
              }
            });
          } else {
            this.numActualUser = result.actualUser;
            this.openRequestedUsersDialog();
          }
        }
      });
    }
  }

  openAddActionsDialog(dataValues?): void {
    const dialogRef = this.dialog.open(AddActionComponent, {
      data: {},
    });

    let form = [...this.addForm];

    if (dataValues) {
      dialogRef.componentInstance.editId = dataValues._id;

      form = form.map((formItem) => {
        if (dataValues[formItem.name]) {
          return (formItem = {
            ...formItem,
            default: dataValues[formItem.name],
          });
        }

        return formItem;
      });
    }

    dialogRef.componentInstance.dataModel = form;

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.addEvent.emit(result);
      }
    });
  }

  edit(dataModel) {
    console.info("EDIT", dataModel);
    this.openDialog(dataModel);
  }

  delete(id) {
    const confirmation = this.dialog.open(ConfirmationComponent);
    confirmation.componentInstance.message = "table.confirmation_message";
    confirmation.afterClosed().subscribe((result) => {
      if (result) {
        this.deleteEvent.emit(id);
      }
    });
  }

  generateSmartelo(dataModel) {
    this.editEvent.emit({
      id: dataModel._id,
      onlyDownload: dataModel.smarteloFile,
    });
  }

  details(dataModel) {
    this.detailsEvent.emit(dataModel);
  }

  results(dataModel) {
    this.resultsEvent.emit(dataModel);
  }

  select() {
    this.onSelectSubmit.emit(this.selection.selected);
  }
}
