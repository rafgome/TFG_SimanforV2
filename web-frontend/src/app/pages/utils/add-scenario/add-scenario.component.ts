import { Component, Input, OnInit } from "@angular/core";
import { MatDialogRef, MatDialog } from "@angular/material";
import { TableDialogComponent } from "../table/table.component";
import { MatSnackBar } from "@angular/material/snack-bar";
import { Model } from "../../../_models/model";
import { Inventory } from "../../../_models/inventory";
import { ModelService } from "../../../_services/model.service";
import { InventoryService } from "../../../_services/inventory.service";
import { ScenarioService } from "../../../_services/scenario.service";

class StepModel {
  name?: string;
  description?: string;
  model?: Model;
  variables?: object;
}

@Component({
  selector: "app-add-scenario",
  templateUrl: "./add-scenario.component.html",
  styleUrls: ["./add-scenario.component.scss"],
})
export class AddScenarioComponent implements OnInit {
  @Input() dataModel?: any;
  projectionModels: Model[];
  cuttingModels: Model[];
  inventories: Inventory[];
  header: string[];
  steps: StepModel[];
  inventory: Inventory;
  projectionModel: Model;

  public loading = false;

  constructor(
    public dialogRef: MatDialogRef<AddScenarioComponent>,
    public dialog: MatDialog,
    private modelService: ModelService,
    private inventoryService: InventoryService,
    private scenarioService: ScenarioService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    if (!this.dataModel) {
      this.steps = [
        {
          name: "",
          description: "",
          variables: {},
        },
      ];
    } else {
      this.steps = this.dataModel.steps;
    }

    this.modelService.getCuttingModels().subscribe(
      (resp) => {
        this.cuttingModels = resp.data;
      },
      (error) => {
        console.error(error);
      }
    );

    this.modelService.getProjectionModels().subscribe(
      (resp) => {
        this.projectionModels = resp.data;
      },
      (error) => {
        console.error(error);
      }
    );

    this.inventoryService.getInventories().subscribe(
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

  addStep(prevIndex): void {
    this.steps.splice(prevIndex + 1, 0, {
      name: "",
      description: "",
      variables: {},
    });
  }

  removeStep(index): void {
    if (this.steps.length > 1) {
      this.steps.splice(index, 1);
    }
  }

  selectProjectionModelDialog(): void {
    const dialogRef = this.dialog.open(TableDialogComponent, {
      height: "500px",
      width: "900px",
      data: {
        tableTitle: "models",
        rowButtons: [],
        tableBody: this.projectionModels,
        tableHeader: [
          "name",
          "type",
          "status",
          "modelClass",
          "specie",
        ],
        selectable: true,
        allowMultiSelect: false,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (!result) {
        return;
      }

      const model = result[0];

      if (!model) {
        return;
      }

      this.projectionModel = model;

      this.steps.forEach((step) => {
        if (step.model.type === "projection") {
          step.model = model;
        }
      });
    });
  }

  applyProjectionModel(stepIndex): void {
    if (!this.projectionModel) {
      this.snackBar.open(
        "You need to define a projection model before.",
        "Close",
        {
          duration: 6000,
          horizontalPosition: "center",
          verticalPosition: "top",
        }
      );
    }

    this.steps[stepIndex].model = this.projectionModel;
  }

  selectCuttingModelDialog(stepIndex): void {
    const dialogRef = this.dialog.open(TableDialogComponent, {
      height: "500px",
      width: "900px",
      data: {
        tableTitle: "models",
        rowButtons: [],
        tableBody: this.cuttingModels,
        tableHeader: [
          "name",
          "type",
          "status",
          "modelClass",
          "specie",
        ],
        selectable: true,
        allowMultiSelect: false,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (!result) {
        return;
      }

      const model = result[0];

      if (!model) {
        return;
      }

      this.steps[stepIndex].model = model;
    });
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
      steps: this.steps,
      inventory: this.inventory,
      projectionModel: this.projectionModel,
    });
  }

  run(_id): void {
    this.loading = true;

    this.scenarioService.runScenario(_id).subscribe(
      (data) => {
        this.loading = false;
        this.dialogRef.close();
        console.log(data);
      },
      (error) => {
        this.loading = false;
        this.dialogRef.close();
        console.log(error);
      }
    );
  }

  changeField(field, index, ev): void {
    this.steps[index][field] = ev.target.value;
  }

  changeVariable(field, index, value): void {
    const isANumber = !isNaN(value);
    if (isANumber) {
      value = parseInt(value);
    }
    this.steps[index].variables[field] = value;
  }
}
