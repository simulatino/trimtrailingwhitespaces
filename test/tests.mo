within ;
model LargeModel "Model of a hydronic heating system with energy storage"
  extends Modelica.Icons.Example;

  Modelica.Blocks.Logical.And and1 "xxx"
    annotation (Placement(transformation(extent={{-82,560},{-62,580}})));

  Modelica.Blocks.Logical.And and2 "xxx"
// Should be removed
    annotation (Diagram(transformation(extent={{664,-170},{684,-150}})));

// Should stay:
  annotation (Diagram(coordinateSystem(preserveAspectRatio=false,extent={{-120,
            -200},{700,600}}),
                         graphics),
Documentation(info="<html>
<p>
xxx
</p>
</html>", revisions="<html>
xxx
</html>"));

// Diagram should be removed:
 annotation (Diagram(graphics),
             Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-100,
            -100},{100,100}}), graphics), Icon(coordinateSystem(
          preserveAspectRatio=false,extent={{-120,-120},{120,120}}), graphics={
          Text(
          extent={{-62,-56},{80,-84}},
          lineColor={0,0,0},
          fillPattern=FillPattern.Solid,
          fillColor={0,0,0},
          textString="Compressor")));

// annotation should be removed:
annotation ( Icon(coordinateSystem(extent={{-100,-100},
            {100,100}})));
// Diagram should be removed:
annotation (Diagram(coordinateSystem(extent={{-100,-100},{100,100}},
          preserveAspectRatio=false),
                      graphics), Icon(coordinateSystem(extent={{-100,-100},
            {100,100}})));

end LargeModel;
